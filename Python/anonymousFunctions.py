# Also known as Lambda functions
# Example of an NON anonymous function
def identifier(data, type):
    return data[type]

def who(data, identify):
    return identifier(data, "name")

user = { 'name': "Jose", 'surname': "Loko"}
print(who(user,None))

# Or  as an argument
def identifier2(data, type):
    return data[type]

def who2(data, identify):
    return identify(data, "name")

user = { 'name': "Jose", 'surname': "Loko"}
print(who(user,identifier2))

# Or  as an lambda function (anonymous)

def who3(data, identify):
    return identify(data)

user = { 'name': "Jose", 'surname': "Loko"}
print(who(user,lambda x: x['name']))