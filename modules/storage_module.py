# inital test for hard drive detuner
import time

intensityFileAmount = [10, 25, 50, 250, 500]
demoTime : int = 10

def connect_storage(intensity : int = 1):
    intensity = max(1, intensity)
    intensity = min(5, intensity)
    
    print("Intensity is", intensity)
    
    intensityLoop = intensityFileAmount[intensity]
    
    for repeat in range(demoTime * 1000):
    
        for i in range(intensityLoop): #Goes through every file and removes the contents
            with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
                file.write("")
        
        for i in range(intensityLoop): #Creates a glorp cat image for every text file
            with open("glorp_clone_" + str(i + 1) + ".txt", "w") as file:
                
                with open("modules/resources/glorp.txt", "r") as file2:
                    value = str(file2.read())
                    file.write(value)
                    file.write(value)
                    file.write(value)
                    file.write(value)
                    file.write(value)
                    file.write(value)
                    file.write(value)
                    file.write(value)
                    file.write(value)
                    file.write(value)
        
        time.sleep(0.001)

    return {"success": True, "message": f"Storage ready (intensity {intensity})"}
