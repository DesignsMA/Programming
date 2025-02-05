numbers = list(range(10)) #list from 0-10
doubledNumbers = [x*2 for x in numbers] #create a new list by multiplying each number in the original list by two.  
phrases = [f"Im {age} years old" for age in doubledNumbers]
namesList = ["John", "Jane", "Tom", "Alice"]
namesLower = [name.lower() for name in namesList]

#With Conditional

friends = ["John", "Jane", "Tom", "Alice"]
guests = ["john", "Tom", "alice"]

lowerFriends = [friends.lower() for friends in friends]
presentFriends = [name.capitalize() for  name in guests if name.lower() in lowerFriends]

#printing

print(f"Without conditionals: \n{numbers}\n{doubledNumbers}\n{phrases}\n{namesList}\n{namesLower}\n")

print(f"With conditionals: \n{friends}\n{guests}\n{presentFriends}")

#Set Comprehension and dictionaries

friends2 = { "john", "jane", "tom", "alice", "mike"}
guests2 = { "mike", "john", "alice"}
friendsPresent = {name.capitalize() for name in friends2 & guests2}