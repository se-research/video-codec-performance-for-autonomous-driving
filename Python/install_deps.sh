#!/bin/bash
sudo apt-get install python3.6 -y

python3 -m venv ~/py3-environments/coordinator
source ~/py3-environments/coordinator/bin/activate

pip3 install -r requirements.txt
