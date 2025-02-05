import file_operations
#or from directory_w/o_spaces.module import function1, function 2, ...
from file_operations import save_to_file, read_file

import json

file = "Files Python Programs.py/imports/data.txt"
weapons = { 'weapons': [ # set of list of dictionaries
    {'name':'Sword', 'damage':5},
    {'name':'Axe','damage':7}
]}

throwables = { "throwables": [
    {"name":"Shuriken",'range':10,'thrown_at':30, 'on_hit':'kill'},
    {"name":"Juice Can","range":20,"thrown_at":40, 'on_hit':'stun'}
]}

save_to_file(file,json.dumps(weapons, indent=6)) # save weapons to data.txt as JSON format in the file data.txt
print(read_file(file))
file_operations.save_to_file(file,'\n'+json.dumps(throwables, indent=6),'w+') # append to the end of the file
json_final = file_operations.read_file(file) #or given the object file_operations
print(json_final)

print(json.loads(json_final)['throwables']) # access a specific part of the JSON data
