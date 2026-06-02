# Los type hints son simplemente para mejorar legibilidad y la experiencia al escribir el codigo,
# python ignora completamente los type hints, son solo para los desarrolladores y para que el editor
# de codigo pueda autocompletar o sugerir cosas.  (Aunque puedes importar modulos q si trabajan con los type)
def full_name(first_name: str, second_name: int, age: int):
    return "Your full name is: " + first_name.title() + " " + second_name.capitalize() + str(age)

print(full_name("jOSTIn", "Lenin", 17))