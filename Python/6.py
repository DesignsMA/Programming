import sys
 # Load the sys module
if len(sys.argv) != 2:
     # Check number of command line arguments :
    print("Please supply a filename")
    raise SystemExit(1)
f = open(sys.argv[1]) #abrir archivo con nombre sys.argv[1]
 # Filename on the command line
lines = f.readlines()
 # Read all lines into a list
f.close()

# Convert all of the input values from strings to floats
fvalues = [float(line) for line in lines]
# Print min and max values
print ("The minimum value is ", min(fvalues))
print ("The maximum value is ", max(fvalues))
