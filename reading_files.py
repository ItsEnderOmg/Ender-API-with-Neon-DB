
import sqlite3

print("hello world")

with open("index.txt", "r") as archivo:
    for linea in archivo:
        print(linea.strip())