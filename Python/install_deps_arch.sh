#!/bin/bash
#pacman -S python
pacman -S tk
pacman -S python-virtualenv

python3 -m venv ~/joacimerik/py3-environments/coordinator
source ~/joacimerik/py3-environments/coordinator/bin/activate

pip3 install -r requirements.txt
