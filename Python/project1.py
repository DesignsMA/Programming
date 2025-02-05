import os
def order(movies, tipo, limit):
    arrayOfOrder = [i for i in range(limit)]
    if tipo == 'name':
        order_tipo = [str(movies[i][tipo])[0] for i in range(limit)]
    else: 
        order_tipo = [int(movies[i][tipo]) for i in range(limit)]
    i =  0
    # Traverse through all array elements 
    for i in range(limit):
        # Find the minimum element in remaining  
        # unsorted array 
        min_idx = i 
        for j in range(i+1, limit): 
            if order_tipo[arrayOfOrder[min_idx]] > order_tipo[arrayOfOrder[j]]: 
                min_idx = j 
        arrayOfOrder[i], arrayOfOrder[min_idx] = arrayOfOrder[min_idx], arrayOfOrder[i]
    
    return arrayOfOrder

def printMovies(movies, limit, order):
    print("-------------------------------")
    for i in range(limit):
        print(f"{movies[order[i]]['name']} | {movies[order[i]]['year']}\nDirected by: {movies[order[i]]['director']}\n")
    print("-------------------------------")

def binarySearch(movies, search, lim, order):
    start, end = 0, lim
    mid = (start + end) // 2
    if search == movies[order[mid]]['year']:
        return mid 
    while not(search == movies[order[mid]]['year']) and start <= end:
        if search < movies[order[mid]]['year']:
            end = mid-1
        else:
            start = mid+1
        mid = (start + end) // 2
    if start <= end:
        print(f"{movies[order[mid]]['name']} | {movies[order[mid]]['year']}\nDirected by: {movies[order[mid]]['director']}\n")
        return mid
    else:
        return -1

def linearSearch(movies, search, lim):
    for i in range(lim):
        if movies[i]['name'] == search:
            print(f"{movies[i]['name']} | {movies[i]['year']}\nDirected by: {movies[i]['director']}\n")
            return i
    return -1

    
# MAIN
movies = [] 
movie = {
'name': None,
'director': None,
'year': None
}
opc = 0
limit = 1
arrayOfOrder = [i for i in range(10)]
orderedByName, orderedByYear = [], []

while True:
    movie['name'] = input("Enter Movie Name: ").capitalize()
    movie['director'] =  input("Enter Director's name: ").capitalize()
    movie['year'] = int(input("Enter Year Released: "))
    movies.append(movie.copy())
    limit += 1
    if  not (input("Do you want to add more? Y/N ") == 'N'):
        continue
    else:
        break
os.system('cls' if os.name == 'nt' else 'clear')

orderedByName = order(movies, 'name', limit-1)
orderedByYear = order(movies, 'year', limit-1)
print(orderedByName)
print(orderedByYear)
print(arrayOfOrder)
printMovies(movies, limit-1, arrayOfOrder)
while True:
    print("1. Order by name\t 2. Order by year\t3. Search\t4. Exit")
    opc = int(input("Enter an option: "))
    match opc:
        case 1:
            printMovies(movies, limit-1, orderedByName)
            continue
        case 2:
            printMovies(movies, limit-1, orderedByYear)
            continue
        case 3:
            opc = int(input("1. By name\t2.By year"))
            if opc == 1:
                if linearSearch(movies,input("Name: ").capitalize(), limit-1) == -1 :
                    print("Movie Not Found.")
            elif opc == 2:
                if binarySearch(movies,int(input("Year: ")),limit-2, orderedByYear) == -1 :
                    print("Movie Not Found.") 
        case 4:
            break
    
# END OF  MAIN