# ImagingPlan
Get asteroid measurements in the usual MPC format, output a plot on which future asteroid imaging measurements can be planned.

## Usage: 

Running this the following command:

``` python src/PlanningTool.py ```

will produce a plot which represents the input data (``` data/mpc_data.txt```) plotted against a stellar backgroud. The input data is given in the usual IAU MPC format, and the asteroids' headings are represented by arrows. The telescope's FOV is represented by a blue rectangle. The configuration file which can be changed to modify the plotting parameters (observatory code, telescope FOV, filenames) is located in ```src/Config.py```. 

By clicking on the plot, the FOV centre coordinates are saved in ```data/saved_coordinates.txt``` and their modified version in ```data/saved_coord_telescope.txt```. 
