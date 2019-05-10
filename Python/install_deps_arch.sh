#!/bin/bash
pacman -S --noconfirm python
pacman -S --noconfirm tk
pacman -S --noconfirm python-virtualenv

python3 -m venv ~/py3-environments/coordinator
source ~/py3-environments/coordinator/bin/activate

pip3 install -r requirements.txt