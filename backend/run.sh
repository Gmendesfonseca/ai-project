#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install flask flask-cors pytest scipy
python -m flask run
