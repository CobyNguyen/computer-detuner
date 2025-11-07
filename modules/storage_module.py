# inital test for hard drive detuner

for repeat in range(1000):

    for i in range(3):
        with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
            with open("resources/glorp.txt", "r") as file2: #path for glorp not tested
                value = str(file2.read())
                file.write(value)

    for i in range(3):
        with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
            file.write("")
