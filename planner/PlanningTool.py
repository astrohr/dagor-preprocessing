""" Usage: PlanningTool.py (--ours | --finder)"""

from docopt import docopt
import random
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from matplotlib.patches import Rectangle

import ReadCatalog as rcal
import ReadQuery as rquer
import FetchData as fdata
import ParseLib as plib

from Config import config as cfg


def findPlotBorders(object_dict):
    """ Find the minimum and maximum RA and Dec from an object_dict dictionary. """

    # Init heaps
    ra_arr = []
    dec_arr = []

    # Get all dictionary values
    values = object_dict.values()

    # Fill heaps
    for arr in values:
        ra_arr.extend(arr[1])
        dec_arr.extend(arr[2])

    # Find min and max of both RA and Dec
    ra_min, ra_max = min(ra_arr), max(ra_arr)
    dec_min, dec_max = min(dec_arr), max(dec_arr)

    # Averages
    ra_avg = np.average(ra_arr)
    dec_avg = np.average(dec_arr)

    # Find the maximum span
    span_max = max(ra_max - ra_min, dec_max - dec_min) * 1.2

    # Redo the min and max
    ra_min = ra_avg - span_max/2
    ra_max = ra_avg + span_max/2

    dec_min = dec_avg - span_max/2
    dec_max = dec_avg + span_max/2

    # Return the values
    return ra_min, ra_max, dec_min, dec_max


class PlanningTool(object):

    def __init__(self, cal_dir, cal_name, data_dir, data_name, query_dir, query_name, save_dir, save_name, \
        x_span, y_span, lim_mag, ours=True):

        # Form the query
        if ours == True:
            fdata.sData2Query(data_dir, data_name, query_dir, query_name)

        else:
            fdata.sFinder2Query(data_dir, data_name, query_dir, query_name)

        # Load the query
        self.object_dict = rquer.readQuery(query_dir, query_name)

        # Init parameters
        self.save_dir = save_dir
        self.save_name = save_name

        self.x_span = x_span
        self.y_span = y_span

        self.lim_mag = lim_mag

        # Find the plot limits
        self.ra_min, self.ra_max, self.dec_min, self.dec_max = findPlotBorders(self.object_dict)

        # Load the catalog
        self.star_catalog = rcal.loadGaiaCatalog(cal_dir, cal_name, lim_mag=self.lim_mag, ra_min=self.ra_min, \
            ra_max=self.ra_max, dec_min=self.dec_min, dec_max=self.dec_max)

        # Construct color array
        color_arr = cm.nipy_spectral(np.linspace(0.2, 1, len(self.object_dict)))
        color_order = random.sample(range(len(color_arr)), len(color_arr))
        self.color_arr = color_arr[color_order]

        # Init plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        # Plot stars
        self.ax.scatter(self.star_catalog[:, 0], self.star_catalog[:, 1], \
            s=(2.512**(-self.star_catalog[:, 2])*1500), color='black')


        # Plot asteroids
        for i, object_i in enumerate(self.object_dict):
            
            # Extract coordinates and data
            date_str_arr, ra_arr, dec_arr, pa_arr = self.object_dict[object_i]
            color = self.color_arr[i]

            for i, date_str, ra, dec in zip(range(len(date_str_arr)), date_str_arr, ra_arr, dec_arr):

                # Scatter plot, label only if this is the first object in the series              
                if i == 0:
                    self.ax.scatter(ra, dec, c=color, marker='x', label=object_i)
                elif i == 2:
                    self.ax.scatter(ra, dec, c=color, marker='x')
                    pa = np.deg2rad(pa_arr[i + 1])
                    r = np.sqrt((ra - ra_arr[i+1])**2 + (dec-dec_arr[i+1])**2)
                    self.ax.arrow(ra, dec, r*np.sin(pa), r*np.cos(pa), width=0.01)
                    print(object_i, r, pa)
                elif i == 1:
                    self.ax.scatter(ra, dec, c=color, marker='x')
                if i != 3:
                    self.ax.annotate(date_str, (ra, dec), xycoords='data', color='r')


        # Label axes
        self.ax.set_xlabel('RA [deg]')
        self.ax.set_ylabel('Dec [deg]')

        # Legend
        self.legend = self.ax.legend(loc='upper right', fontsize='x-small')

        # Save plot limits
        self.x_min, self.x_max = self.ax.get_xlim()
        self.y_min, self.y_max = self.ax.get_ylim()

        # Plot center
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2

        # Offsets between the rectangle center and lower left corner
        self.x_off = self.x_span/2
        self.y_off = self.y_span/2

        # Init FOV rectangle
        self.fov_rect = Rectangle((self.x_center - self.x_off, self.y_center - self.y_off), self.x_span, self.y_span, \
            fill=True, alpha=0.5, facecolor='blue', edgecolor='black', linewidth=1)

        # Coordinates to which the FOV rectangle is moved
        self.new_x = None
        self.new_y = None

        # Where the selected rectangle positions and names are saved
        self.name_arr = []
        self.x_arr = []
        self.y_arr = []

        # Plotted uncertainties
        self.uncertainties_arr = None

        self.ax.add_patch(self.fov_rect)

        # Register mouse/keyboard events
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.onMouseMotion)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.onMousePress)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.onKeyPress)
        
        # Set tight layout
        self.fig.tight_layout()
        self.ax.margins(0)
        self.ax.set_aspect('equal')
        self.ax.figure.canvas.draw()


    def onMouseMotion(self, event):
        ''' Evokes when the mouse is moved. Moves the rectangle. '''

        # Don't do anything is the mouse is not inside the plot
        if event.inaxes != self.fov_rect.axes: return

        # Save plot limits
        self.x_min, self.x_max = self.ax.get_xlim()
        self.y_min, self.y_max = self.ax.get_ylim()

        # Read new cursor position
        self.new_x = event.xdata
        self.new_y = event.ydata

        # Clip the values so the rectangle is always inside the plot
        self.new_x = np.clip(self.new_x, self.x_min + self.x_off, self.x_max - self.x_off)
        self.new_y = np.clip(self.new_y, self.y_min + self.y_off, self.y_max - self.y_off)

        # Move the rectangle
        self.fov_rect.set_xy((self.new_x - self.x_off, self.new_y - self.y_off))

        # Update plot
        self.ax.figure.canvas.draw()


    def onMousePress(self, event):
        ''' Evokes when the mouse button is pressed. Saves the rectangle coordinates. '''

        # Don't do anything is the mouse is not inside the plot
        if event.inaxes != self.fov_rect.axes: return

        # Read new cursor position
        self.onMouseMotion(event)

        # Save the position
        self.x_arr.append(self.new_x)
        self.y_arr.append(self.new_y)

        # Get the object name
        for i, object_i in enumerate(self.object_dict):
            val_arr = self.object_dict[object_i]
            ra_arr, dec_arr = val_arr[1], val_arr[2]
            ra_avg = np.average(ra_arr)
            dec_avg = np.average(dec_arr)

            if ra_avg > self.ra_min and ra_avg < self.ra_max and \
                dec_avg > self.dec_min and dec_avg < self.dec_max:

                self.name_arr.append(object_i)
                break

        # Save the arrays
        np.savetxt(self.save_dir + self.save_name, np.c_[self.name_arr, self.x_arr, self.y_arr], \
            fmt='%7.7s %9.9s %9.9s')

        # Draw selected rectangle
        rect = Rectangle((self.new_x - self.x_off, self.new_y - self.y_off), self.x_span, self.y_span, \
            fill = True, alpha=0.5, facecolor='green', edgecolor='black', linewidth=1)

        self.ax.add_patch(rect)      

        # Update plot
        self.ax.figure.canvas.draw()


    def onKeyPress(self, event):
        """ Evokes when a key is pressed. """

        key = event.key

        # Show uncertainties
        if (key == 'u') or (key == 'U'):

            # Go through all objects
            for i, object_i in enumerate(self.object_dict):

                # Get all uncertainties
                uncertainties_arr = fdata.getUncertainties(object_i)

                val_arr = self.object_dict[object_i]
                ra_arr, dec_arr = val_arr[1], val_arr[2]

                # Get current RA and Dec
                if len(ra_arr) and len(dec_arr): 

                    ra_curr, dec_curr = ra_arr[0], dec_arr[0]

                    # Convert uncertainties to float
                    ra_uncertainties = uncertainties_arr[:, 0].astype('float')
                    dec_uncertainties = uncertainties_arr[:, 1].astype('float')
                    sign_arr = uncertainties_arr[:, 2]

                    # Form colors array
                    color_rgb_arr = []

                    for sign in sign_arr:
                    
                        # Get object color
                        color = self.color_arr[i]

                        # Form lighter and darker color
                        rgb_darker_color = col.to_rgb(color)
                        rgb_lighter_color = list([c + 0.1 for c in rgb_darker_color])

                        if sign == '!':
                            color_rgb_arr.append(rgb_darker_color)

                        elif sign == '!':
                            color_rgb_arr.append(rgb_lighter_color)


                    # Add uncertainties to center to get coordinates
                    ra_coords = ra_uncertainties + ra_curr
                    dec_coords = dec_uncertainties + dec_curr

                    # Update plot limits
                    self.ax.set_xlim(min(ra_coords), max(ra_coords))
                    self.ax.set_ylim(min(dec_coords), max(dec_coords))

                    self.ax.set_aspect('equal')

                    # Plot uncertainties
                    uncertainties_i = self.ax.scatter(ra_coords, dec_coords, color=color_rgb_arr, marker='o', s=1)

                    self.uncertainties_arr.append(uncertainties_i)

        # Hide uncertainties
        if (key == 'h') or (key == 'H'):

            if self.uncertainties_arr is not None:

                for artist in self.uncertainties_arr: 
                    artist.remove()

        # Update plot
        self.ax.figure.canvas.draw()


if __name__ == '__main__':

    arguments = docopt(__doc__)

    ours = arguments['--ours']

    if ours == True:
        data_dir = cfg.OURS_DIR
        data_name = cfg.OURS_NAME

    else:
        data_dir = cfg.FINDER_DIR
        data_name = cfg.FINDER_NAME

    # Create tool instance
    pln = PlanningTool(cfg.CAL_DIR, cfg.CAL_NAME, data_dir, data_name, cfg.QUERY_DIR, cfg.QUERY_NAME, cfg.SAVE_DIR, cfg.SAVE_NAME, \
        cfg.X_SPAN, cfg.Y_SPAN, cfg.LIM_MAG, ours=ours)

    # Show plot
    plt.show()

    # Convert raw coordinates to telescope format
    plib.parseRaw(cfg.SAVE_DIR, cfg.SAVE_NAME, cfg.FINAL_DIR, cfg.FINAL_NAME)