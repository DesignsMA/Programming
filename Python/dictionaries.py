# Dictionaries and lists are two main data structures in Python for collecting data.
#
# Differences:
#   1. Data structure:
#      - Dictionary: unordered collection of key-value pairs, where each key must be unique
#        and is associated with a corresponding value.
#      - List: ordered collection of elements, where each element can be a value of any type.
#   2. Access:
#      - Dictionary: accessed using keys.
#      - List: accessed using integers.
#   3. Mutability: Both dictionaries and lists are mutable, meaning they can be changed.
#   4. Order of elements: The order of elements in a dictionary is not guaranteed,
#      while the order of elements in a list is maintained.
#   5. Duplicate keys: In a dictionary, keys cannot be duplicated, whereas in a list,
#      duplicate elements can be present.

names = ["John", "Mike", "Anne"] #lists
lastSeen = [8,12,5]

friendsLastSeen = { names[i]: lastSeen[i] for i in range(len(names)) }  #dictionaries
print(friendsLastSeen)
print("Zip: ", *zip(names, lastSeen)) #pointer, we access to its content
friendsLastSeen = dict(zip(names, lastSeen))                            #another way to create a dictionary from two lists
print("Dict from zip ", friendsLastSeen)