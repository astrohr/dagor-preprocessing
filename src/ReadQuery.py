import os

def readLine(line):
	""" Reads out a line from the ephemeris file, returns time, position and position angle. 
		
		Arguments:
			line: [string] Ephemeris line.

		Return:
			param_tup: [tuple of 4 elements] Tuple containing the date [string], RA, Dec and PA [floats]. 
	"""

	# Extract the data as strings
	date_str = line[8:13]
	ra_str = line[17:24]
	dec_str = line[26:33]
	pa = line[60:65]

	# Convert RA string to degrees
	ra_deg = float(ra_str) * 15

	# Determine the Dec sign
	sign = dec_str[0]

	# Convert Dec string to degrees
	dec_deg = float(dec_str[0:])

	if sign == '-':
		dec_deg *= -1

	# Convert PA string to float
	pa_deg = float(pa)

	param_tup = (date_str, ra_deg, dec_deg, pa_deg)

	return param_tup


def readQuery(query_dir, query_name):
	""" Read a query, output a dict containing the data. 
		
		Arguments:
			query_dir: [string] Where the query is located. 
			query_name: [string] Name of the query file (*.txt). 
	
		Return:
			query_dict: [dictionary] Dictionary containing the data. 
				Shape: {object_string: [date_str_arr, ra_deg_arr, dec_deg_arr, pa_deg_arr]}
	"""

	# Get the absolute query path
	query_path = os.path.join(query_dir, query_name)

	print("Reading query results...")

	# Extract all objects and line indices
	objects = []
	borders = []
	
	with open(query_path, 'r') as query:

		for i, line in enumerate(query):

			# Check if this is the line containing the object name
			if line[0:6] == 'Object':
				
				# Extract the object string
				line = line.strip()
				new_object = line[16:len(line)]
				
				borders.append(i)
				objects.append(new_object)

	# Read all lines from the file
	lines = []
	
	with open(query_path, 'r') as query:
		lines = query.readlines()

	# Extract all the ranges
	ranges = []
	for i in range(len(borders) - 1):

		border_a = borders[i]
		border_b = borders[i + 1]

		ranges.append((border_a + 5, border_b - 1))

	# Add last range
	ranges.append((borders[len(borders)-1] + 5, len(lines)))

	# Extract the lines selected by the ranges
	selected_lines = []
	
	for range_i in ranges:

		selected_lines.append(lines[range_i[0]-1 : range_i[1]])

	# Form the return dictionary
	query_dict = {}
	
	for i, entry in enumerate(selected_lines):

		date_arr = []
		ra_arr = []
		dec_arr = []
		pa_arr = []

		query_dict[objects[i]] = []

		# Read line and append to array
		for line in entry:
			
			date, ra, dec, pa = readLine(line)

			date_arr.append(date)
			ra_arr.append(ra)
			dec_arr.append(dec)
			pa_arr.append(pa)

		# Form the key-value pair
		query_dict[objects[i]] = [date_arr, ra_arr, dec_arr, pa_arr]


	return query_dict


if __name__ == '__main__':
	
	object_dict = readQuery('./', 'query.txt')
	print(object_dict)