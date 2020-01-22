import main

i = 0
while i in range(5):
    res = main.run(i)
    i += 1
    if res == "I'm done":
        break
    else:
        pass