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
garage.add_car(ford)
print(len(garage))  # Outputs: 0 (No cars added yet.)
print(garage.cars)


