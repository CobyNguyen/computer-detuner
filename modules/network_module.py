import time
import requests   #pip3 install requests on vs terminal

def slowdown(url, pause=4.0):   
  print("checking internet connection. Be patient.")
  time.sleep(pause)   #simulating slow network response
  requests.get(url)
  
  
  
  
  

