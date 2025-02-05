class MyCustomError(TypeError):
    """This is a doc-string, is used as a way to explain parts of yout class or whole .py program, can be accessed with error.__doc__"""
    def __init__(self, message, code) -> None:
        super().__init__(f'{message} | Error code: {code}') #we access the init method from the parent class (TypeError) 
        self.code = code                            #and pass our custom arguments to it, we create a copy of TypeError
                                                    #in order to do so

print(TypeError().__doc__)                         #we can access
print(MyCustomError("Idk", 500).code,"\n",MyCustomError("Idk", 500).__doc__)   #to

class Car:
    def __init__(self, make: str, model: str) -> None:
        self.make = make
        self.model = model
    
    def __repr__(self) -> str: #Text retuned  when object is called with print() or str()
        return f'<Car {self.make} {self.model}>'

class Garage:
    def __init__(self):
        self.cars = []
    
    def __len__(self):
        return len(self.cars)
    

    def add_car(self, car: Car) -> None: 
        if not isinstance(car,  Car):
            raise TypeError(f"Tried to add a'{car.__class__.__name__}' to the garage, but you can only add 'Car' objects")
        self.cars.append(car)
    
# -------------------- MAIN -------------------- #
ford = Car("Ford", "Fiesta")
garage = Garage()
print(ford)
try: #Forgiving  way of adding non-Cars into the garage
    garage.add_car(ford)
except TypeError:
    print("\nGiven argument was not of type 'Car'.")
except ValueError:
    print('Something caused an error (value error)')
finally:
    print(len(garage), "Cars currently on the garage") 
print(garage.cars)
