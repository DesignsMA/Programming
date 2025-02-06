import sys

if  len( sys.argv ) < 2:
    print("Provide the csv records file name")
    raise SystemExit(1)

people = []
try:
    for line in open(sys.argv[1]):
        data = line.split(',') #divide in commas
        name = data[0]
        age = data[1]
        city = data[2]
        person = (name,age,city)
        people.append(person)

    for name, age, city in people:
        print(f"{name} | {age} | {city}")
except OSError:
    print("File doesn't exist or is unsupported.")
    raise SystemExit(1)
