my_file = open("Files Python Programs.py/data.txt", 'r')
file_content = my_file.read()

my_file.close()  

print(file_content)  # Output: Hello,
my_file = open("Files Python Programs.py/data.txt", 'r')
file_content = my_file.read()
my_file.close()
my_file_write = open("Files Python Programs.py/data.txt", 'w')
my_name = input("Enter your name: ")
my_file_write.write(file_content + '\n' + ' - ' + my_name )
my_file_write.close()

