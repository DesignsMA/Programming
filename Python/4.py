for num in range(2,10):
    for x in range(2,num):  #se checa de 2 hasta el  número actual (no igual).
        if num % x == 0: #se checa que el numero actual sea divisible entre un numero de 2-num.
            print(f"{num} equals to {x} * {num//x}")
            break
    else:    #Si no es divisible entre ningun numero
        print(f"{num} is a prime number.")
        
    