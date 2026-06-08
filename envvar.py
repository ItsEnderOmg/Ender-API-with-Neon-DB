import os

name = os.getenvar("SAY_MY_NAME", "stupid")

print(f"You're {name} from Python")