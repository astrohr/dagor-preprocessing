import random
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Rectangle

import ReadCatalog as rcal
import ReadQuery as rquer
import FetchData as fdata

# Location of the star catalog
cal_dir = '../data/'
cal_name = 'gaia_dr2_mag_11.5.npy'

# Location of the MPC data
data_dir = cal_dir
data_name = 'mpc_data.txt'

# Location of the query results
query_dir = cal_dir
query_name = 'query_results.txt'

# Where the imaging coordinates are saved
save_dir = cal_dir
save_name = 'saved_coordinates.txt'

# Ask the user for limiting magnitude and FOV size
lim_mag = float(input('Limiting mag: '))
x_span = float(input('Horizontal FOV size (degrees): '))
y_span = float(input('Vertical FOV size (degrees): '))

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
        x_span, y_span):

        # Form the query
        fdata.sData2Query(data_dir, data_name, save_dir, save_name)

        # Load the query
        self.object_dict = rquer.readQuery(query_dir, query_name)

        # Init parameters
        self.save_dir = save_dir
        self.save_name = save_name

        self.x_span = x_span
        self.y_span = y_span

        # Find the plot limits
        self.ra_min, self.ra_max, self.dec_min, self.dec_max = findPlotBorders(self.object_dict)

        # Load the catalog
        self.star_catalog = rcal.loadGaiaCatalog(cal_dir, cal_name, lim_mag=lim_mag, ra_min=self.ra_min, \
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

        self.ax.add_patch(self.fov_rect)

        # Register mouse/keyboard events
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.onMouseMotion)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.onMousePress)
        
        # Set tight layout
        self.fig.tight_layout()
        self.ax.margins(0)
        self.ax.set_aspect('equal')
        self.ax.figure.canvas.draw()


    def onMouseMotion(self, event):
        ''' Evokes when the mouse is moved. Moves the rectangle. '''

        # Don't do anything is the mouse is not inside the plot
        if event.inaxes != self.fov_rect.axes: return

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

        # Read cursor position
        x_sel = event.xdata
        y_sel = event.ydata

        # Save the position
        self.x_arr.append(x_sel)
        self.y_arr.append(y_sel)

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
        rect = Rectangle((x_sel - self.x_off, y_sel - self.y_off), self.x_span, self.y_span, \
            fill = True, alpha=0.5, facecolor='green', edgecolor='black', linewidth=1)

        self.ax.add_patch(rect)      

        # Update plot
        self.ax.figure.canvas.draw()


if __name__ == '__main__':

    # Instantiate object
    pln = PlanningTool(cal_dir, cal_name, data_dir, data_name, query_dir, query_name, save_dir, save_name, \
        x_span, y_span)

    # Show plot
    plt.show()