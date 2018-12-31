class ConfigStruct(object):
	def __init__(self):
		
		# Location of the star catalog
		self.CAL_DIR = '../data/'
		self.CAL_NAME = 'gaia_dr2_mag_11.5.npy'

		# Location of the MPC data
		self.DATA_DIR = '../data/'
		self.DATA_NAME = 'mpc_data.txt'

		# Location of the query results
		self.QUERY_DIR = '../data/'
		self.QUERY_NAME = 'query_results.txt'

		# Where the RAW imaging coordinates are saved
		self.SAVE_DIR = '../data/'
		self.SAVE_NAME = 'saved_coordinates.txt'

		# Where the imaging coordinates IN TELESCOPE FORMAT are saved
		self.FINAL_DIR = '../data/'
		self.FINAL_NAME = 'saved_coord_telescope.txt'

		# Ask the user for limiting magnitude and FOV size
		self.LIM_MAG = 11.5
		self.X_SPAN = 0.7317
		self.Y_SPAN = 0.7317


config = ConfigStruct()		