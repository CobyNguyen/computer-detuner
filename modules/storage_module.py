# inital test for hard drive detuner
import time

intensityFileAmount = [5, 10, 20, 50, 100]
demoTime : int = 10

def connect_storage(val : int = 1):
    val = max(1, val)
    val = min(5, val)
    
    print("Intensity is", val)
    
    intensity = intensityFileAmount[val]
    
    for repeat in range(demoTime * 10):
    
        for i in range(intensity):
            with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
                file.write("")
        
        for i in range(intensity):
            with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
                
                with open("resources/glorp.txt", "r") as file2: #path for glorp not tested
                    value = str(file2.read())
                    file.write(value)
        
        time.sleep(0.1)
