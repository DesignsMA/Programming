file = open("Files Python Programs.py/csv.txt", 'r')
csv_lines = [line.strip() for line in file.readlines()[1:]]
file.close()

# Split the lines into words and store them as a list of lists, where each sublist is one row from csv_lines
print("Name\tAge\tCareer\t\tUniversity")  # Print header information
for line in csv_lines:
    list_data =  line.split(',')
    print(f"{list_data[0]}\t{list_data[1]}\t{list_data[2]}\t\t{list_data[3]}".title())  # Use comma to split data into individual fields   # Split data by comma
    