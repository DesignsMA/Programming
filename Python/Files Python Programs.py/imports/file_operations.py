def save_to_file(filename: str, data: str, mode:str='w'):
    with open(filename, mode) as file:
        file.write(data)

def read_file(filename: str):
    with open(filename, 'r') as file:
        return file.read()
