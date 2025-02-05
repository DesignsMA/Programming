is_programer = False
name = "John Doe"
name = input("Your Name: ")

while is_programer == False:
    is_programer = input("Are you a programmer? ") == "Yes"
    if is_programer:
        print("congraTULAtons " + name)
    else:
        print("Please try again.")