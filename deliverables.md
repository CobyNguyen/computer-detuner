## Deliverables:

# Main features
- UI that connects/calls modules
- CPU detuner framework
- GPU detuner framework
- Hard Drive detuner framework
- Network detnuer framework
  
 
# UI

Intensity sliders for each module

Can run modules individually and interfaces with each of them so the modules can be run

# Module frameworks

CPU - Runs multiple threads to slow down the CPU and the intensity determines how many threads are run at once

GPU - Draws a bunch of 2d shapes with the intensity determining the resolution and number of shapes

Hard drive - Reads and writes to several files at once to slow down the hard drive with the intensity determining how many files are read/written to at once

Network - Limits the bandwith of network your computer can accept by downloading a bunch of packets with the intensity determining how many packets are requested at once

Each module has the following methods:

  Start(val) takes an integer from 1-5 and determines how many resources the module takes up, then runs the module

# Intensity definitions

  CPU intensity - How many threads are run e.g. (1 = 100, 2 = 250, 3 = 500, 4 = 2000, 5 = 10000)
  
  GPU intensity - Resolution and number of shapes run
  
  Hard Drive intensity - How many files are written to at once e.g. (10 = 5, 2 = 50, 3 = 100, 4 = 250, 5 = 500)
  
  Network intensity - How many packets are requested
  
     
