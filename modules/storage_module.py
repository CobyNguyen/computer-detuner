# inital test for hard drive detuner
import time

intensityFileAmount = [10, 50, 100, 250, 500]
demoTime : int = 10

def connect_storage(intensity : int = 1):
    intensity = max(1, val)
    intensity = min(5, val)
    
    print("Intensity is", val)
    
    moduleIntensity = intensityFileAmount[val]
    
    for repeat in range(demoTime * 1000):
    
        for i in range(moduleIntensity):
            with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
                file.write("")
        
        for i in range(moduleIntensity):
            with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
                
                with open("modules/resources/glorp.txt", "r") as file2: #path for glorp not tested
                    value = str(file2.read())
                    file.write(value)
        
        time.sleep(0.001)
