from pprint import pp
dictionary = {
    'A': [],
    'B': [],
    'C': []  }
enumList = []
for enum in enumerate(dictionary.keys()): #enumerar llaves
    enumList.append(enum)
    pp(enum)
    
pp(enumList)
    
