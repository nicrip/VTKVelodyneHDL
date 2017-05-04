# VTKVelodyneHDL  
Velodyne HDL VTK Driver  

## Dependencies  

### PCAP Library  
sudo apt-get install libpcap-dev  

### VTK Libraries  
sudo apt-get install libvtk5-qt4-dev python-vtk

### Python Libraries
sudo apt-get install python-dev python-numpy  

### Boost Libraries  
sudo apt-get install libboost-all-dev  

## Build  

### Building  
> mkdir build  
> cd build  
> cmake ..  
> make

### Add To Path
Add to your .bashrc  
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/..../path/to/build"  
export LIBRARY_PATH="$LIBRARY_PATH:/..../path/to/build"  
export PYTHONPATH="$PYTHONPATH:/..../path/to/build"  

## Usage  

### Streaming PCAP File  
build/PacketFileSender pcap_file.pcap  

### Python  
test/testVelo.py  
test/testVeloThreading.py  

### C++
(source) test/testVelo.cxx  
(usage) build/testVelo  
