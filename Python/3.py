my_friends = {
    "John": 12,
    "Anne": 19,
    "Mike": 16
}

for name, days in my_friends.items():  #TRANSFORMS a dictionarie into an iterable set [("john",12),...,("name",days)]
    print(f"I saw {name} {days} days ago")

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