
friends = [str(input(f"Enter your friend N-{i+1}: ")).capitalize() for i in range(3)]
friendstxt = open("Files Python Programs.py/friends.txt", 'r')
friends_nearby = [line.strip() for line in friendstxt.readlines()]
friendstxt.close()

nearbytxt = open("Files Python Programs.py/nearby_you.txt", 'w')

for friend in friends:
    for nearby_friend in friends_nearby:
            if nearby_friend == friend:
                print(f"\n{friend} is nearby you.")
                nearbytxt.write(friend+'\n')
                
nearbytxt= open("Files Python Programs.py/nearby_you.txt", 'r')
nearby_content = nearbytxt.read()
nearbytxt.close()
print(nearby_content)