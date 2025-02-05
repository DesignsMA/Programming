numbers = [7,8,4,2,6]
var = 69

for i in numbers:
    print(f"{i} number")
    
print("{var}") #imprime sin literales (variables)
print(f"{var}") #accede al contenido de la variable var

while i < 10: #se conserva i del primer for (no local)
    print(f"{i}")
    i += 1