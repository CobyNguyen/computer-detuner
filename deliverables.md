## Deliverables:

# Main features
- UI that connects/calls modules
- CPU detuner framework
- GPU detuner framework
- Hard Drive detuner framework
- Network detnuer framework
- 
 
# UI
Intensity sliders for each module
Can run modules individually

# Module frameworks
CPU - Runs multiple threads to slow down the CPU
GPU - Runs some intensive shaders to slow down the GPU
Hard drive - Reads and writes to several files at once to slow down the hard drive
Network - Limits the bandwith of network your computer can accept

Each module has the following methods:
  Start(val) takes an integer from 1-5 and determines how many resources the module takes up, then runs the module

# Intensity definitions
  CPU intensity - How many threads are run e.g. (1 = 100, 2 = 250, 3 = 500, 4 = 2000, 5 = 10000)
  GPU intensity - How intensive the shader is which could be defined through a uniform variable e.g. (1 = 50mbps, 2 = 20mbps, 3 = 5mbps, 4 = 1mbps, 5 = 100kbps)
  Hard Drive intensity - How many files are written to at once e.g. (1 = 5, 2 = 10, 3 = 20, 4 = 50, 5 = 100)
  Network intensity - How much bandwith is limited e.g. (1 = 50mbps, 2 = 20mbps, 3 = 5mbps, 4 = 1mbps, 5 = 100kbps)
     
