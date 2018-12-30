import os

def readLine(line):

	date_str = line[0:12]
	ra_str = line[15:25]
	dec_str = line[26:35]

	# Converting ra_str to degrees
	ra_hrs, ra_min, ra_sec = map(float, ra_str.split(' '))
	ra_sec += ra_hrs*3600 + ra_min*60

	ra_deg = float(ra_sec/240)

	# Converting dec_str to degrees
	sign = dec_str[0]

	dec_deg, dec_min, dec_sec = map(float, dec_str[0:].split(' '))
	dec_deg += float(dec_min/60) + float(dec_sec/3600)

	if sign == '-':
		dec_deg *= -1

	return date_str, ra_deg, dec_deg

def readQuery(query_dir, query_name):

	query_path = os.path.join(query_dir, query_name)

	objects = []
	borders = []
	with open(query_path, 'r') as query:
		for i, line in enumerate(query):
			if line[0:6] == 'Object':
				
				line = line.strip()
				new_object = line[11:len(line)]
				
				borders.append(i)
				objects.append(new_object)

	lines = []
	with open(query_path, 'r') as query:
		lines = query.readlines()

	ranges = []
	for i in range(len(borders) - 1):

		border_a = borders[i]
		border_b = borders[i + 1]

		ranges.append((border_a + 8, border_b - 1))

	# Add last range
	ranges.append((borders[len(borders)-1] + 8, len(lines)))

	selected_lines = []
	for range_i in ranges:

		selected_lines.append(lines[range_i[0]-1:range_i[1]])

	query_dict = {}
	for i, entry in enumerate(selected_lines):

		date_arr = []
		ra_arr = []
		dec_arr = []

		query_dict[objects[i]] = []

		for line in entry:
			
			date, ra, dec = readLine(line)

			date_arr.append(date)
			ra_arr.append(ra)
			dec_arr.append(dec)

		query_dict[objects[i]] = [date_arr, ra_arr, dec_arr]

	return query_dict


if __name__ == '__main__':
	
	object_dict = readQuery('./', 'query.txt')
	print(object_dict)