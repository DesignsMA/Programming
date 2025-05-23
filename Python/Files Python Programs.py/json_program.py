import json
file = open("Files Python Programs.py/friends.json", 'r')
print(file)
file_contents = json.load(file) # Reads file and turns it into a dictionary
file.close()

print(file_contents) #dictionary  with the friends data
print(file_contents['friends']) #list of friend dictionaries
print(file_contents['friends'][0]) #dictionary of  friend 1

cars ={ "cars":[
    {"model": "Toyota Camry", "year": 2019, "color": "blue"},
    {"model": "Honda Civic", "year": 2020, "color": "red"}
       ] }

cars_json = open("Files Python Programs.py/cars.json", 'w')
json.dump(cars, cars_json, indent=6) # Writes list of dictionaries to a new .json file
cars_json.close()

# using loads( ) method instead of load( ) method because we are reading from a string not a file
my_json_string = '[{"name": "Alfa Romeo", "released": 1950}]'

incorrect_car = json.loads(my_json_string) # This will throw an error if my_json_string is not formatted correctly as JSON
print(incorrect_car[0]['name'])