import random
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Rectangle

import ReadCatalog as rcal
import ReadQuery as rquer

# Location of the star catalog
cal_dir = './'
cal_name = 'gaia_dr2_mag_11.5.npy'

# Location of the query
query_dir = cal_dir
query_name = 'query.txt'

# Where the imaging coordinates are saved
save_dir = cal_dir
save_name = 'saved_coordinates.txt'

'''
# Ask the user for plot borders, and limiting magnitude
print('All further input values will be required in DEGREES!')
ra_min = float(input('Minimum RA: '))
ra_max = float(input('Maximum RA: '))

dec_min = float(input('Minimum Dec: '))
dec_max = float(input('Maximum Dec: '))

lim_mag = float(input('Limiting mag: '))

x_span = float(input('Horizontal FOV size: '))
y_span = float(input('Vertical FOV size: '))
'''

ra_min, ra_max = 105, 108.5
dec_min, dec_max = 21.7, 25

lim_mag = 11.5
x_span, y_span = 0.7317, 0.7317

class PlanningTool(object):

    def __init__(self, cal_dir, cal_name, query_dir, query_name, save_dir, save_name, ra_min, ra_max, dec_min, dec_max, \
        x_span, y_span):

        self.save_dir = save_dir
        self.save_name = save_name

        self.ra_min = ra_min
        self.ra_max = ra_max

        self.dec_min = dec_min
        self.dec_max = dec_max

        self.x_span = x_span
        self.y_span = y_span

        # Load the catalog
        self.star_catalog = rcal.loadGaiaCatalog(cal_dir, cal_name, lim_mag=lim_mag, ra_min=self.ra_min, \
            ra_max=self.ra_max, dec_min=self.dec_min, dec_max=self.dec_max)

        # Load the query
        self.object_dict = rquer.readQuery(query_dir, query_name)

        # Construct color array
        color_arr = cm.nipy_spectral(np.linspace(0.2, 1, len(self.object_dict)))
        color_order = random.sample(range(len(color_arr)), len(color_arr))
        self.color_arr = color_arr[color_order]


        # Init plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        # Plot stars
        self.ax.scatter(self.star_catalog[:, 0], self.star_catalog[:, 1], \
            s=(2.512**(-self.star_catalog[:, 2])*1000), color='black')

        print(self.object_dict)

        # Plot asteroids
        for i, object_i in enumerate(self.object_dict):
            
            date_str_arr, ra_arr, dec_arr = self.object_dict[object_i]
            color = self.color_arr[i]

            for i, date_str, ra, dec in zip(range(len(date_str_arr)), date_str_arr, ra_arr, dec_arr):
                if ra > ra_min and ra < ra_max and dec > dec_min and dec < dec_max:
                    if i == 0:
                        self.ax.scatter(ra, dec, c=color, marker='x', label=object_i)
                    else:
                        self.ax.scatter(ra, dec, c=color, marker='x')
                    self.ax.annotate(date_str[4:], (ra, dec), xycoords='data', color='r')

            '''
            if min(ra_arr) > ra_min and max(ra_arr) < ra_max and min(dec_arr) > dec_min and max(dec_arr) < dec_max:
                self.ax.scatter(ra_arr, dec_arr, c=color, marker='x', label=object_i)
                self.ax.annotate(date_str_arr, (ra_arr, dec_arr), xycoords='data')
            '''

        # Label axes
        self.ax.set_xlabel('RA')
        self.ax.set_ylabel('Dec')

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

        # Where the selected rectangle positions are saved
        self.x_arr = []
        self.y_arr = []

        self.ax.add_patch(self.fov_rect)

        # Register mouse/keyboard events
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.onMouseMotion)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.onMousePress)
        # self.ax.figure.canvas.mpl_connect('key_press_event', self.onKeyPress)
        # self.ax.figure.canvas.mpl_connect('key_release_event', self.onKeyRelease)
        
        # Set tight layout
        self.fig.tight_layout()
        self.ax.margins(0)
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

        # Save the arrays
        np.savetxt(self.save_dir + self.save_name, np.c_[self.x_arr, self.y_arr])

        # Draw selected rectangle
        rect = Rectangle((x_sel - self.x_off, y_sel - self.y_off), self.x_span, self.y_span, \
            fill = True, alpha=0.5, facecolor='green', edgecolor='black', linewidth=1)

        self.ax.add_patch(rect)      

        # Update plot
        self.ax.figure.canvas.draw()


pln = PlanningTool(cal_dir, cal_name, query_dir, query_name, save_dir, save_name, ra_min, ra_max, dec_min, dec_max, x_span, y_span)
plt.show()