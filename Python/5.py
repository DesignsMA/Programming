
f =  open("notes.txt", "w+") #abrir archivo
f.write("\t\t--NOTES--\n")
print("\t\tPress Ctrl+Z to exit:")
while True:
    try:
        line = input()[:50] #leer cadena de usuario, solo los primeros 50 caracteres

        for i in range(51-len(line)):
            line += '-'
        line += '\n'

        #print(line, file=f) otra forma de escribir en archivo
        f.write(line)
    except EOFError:
        print("\nExiting...\n'notes.txt' was created.")
        f.close()
        exit()