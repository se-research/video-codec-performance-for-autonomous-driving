# video-codec-performance-for-autonomous-driving

## Run in Python virtual environment (venv)
#### Set up virtual environment with dependencies (only has to setup once)
1. cd into `video-codec-performance-for-autonomous-driving/Python`
2. `chmod +x install_deps.sh` Makes shell script executable
3. `./install_deps.sh` Runs shell script that installs all depenecies and creates venv 

#### Adding more datasets
1) Simply put a folder containing the frames in the datasets folder 
(`video-codec-performance-for-autonomous-driving/datasets`)  

_NOTE_
The frames must be PNGs with a resolution of either 2048x1536 (QXGA) or 1392x512.
Every frame of in each dataset must have the same resolution.

#### Run the script
1. `source ~/py3-environments/coordinator/bin/activate` Activates venv
2. `python3 coordinator.py` Runs script in venv
3. `deactivate` Exit venv

#### Generate graphs from existing reports
1. `source ~/py3-environments/coordinator/bin/activate` Activates venv
2. `python3 graph_generator.py <path with datasets>` Generate graphs based on existing reports in provided folder  
 i.e `python3 graph_generator.py /home/user/project123/output/user-2019_05_19-14_40_34`

_NOTE_
The graphs will be generated in <path with datasets>/dataset/<encoder_graphs | joint_graphs | comparison_graphs>
Graphs will be generated in everydata folder

#### Notes
1. In FFE.py: start.delay parameter needs to be changed according to your machine. If the delay is too low 
the error message `404 Client Error: Not Found ("No such container: ...")` will be received for every 
optimization iteration. 

#### Requirements 
- Unix-like OS (tested on Arch Linux 5.0.7, Ubuntu 18.04.02 LTS and MacOS 10.14.5)
- Docker (version > 18) properly installed
- Intel QuickSync H.264 and VP9 support (Kaby Lake, Gemini Lake, Coffee Lake, Cannon Lake or later)

#### Acknowledgement
Christian Berger
The Revere labratory

