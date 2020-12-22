import os

print(os.path.dirname(os.path.abspath(__file__)))

if os.path.isfile("chromedriver"):
    print(True)
else:
    print(False)

print(f"{os.path.dirname(os.path.abspath(__file__))}/chromedriver")
