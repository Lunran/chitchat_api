# What's this?

- Flask API to use Chitchat engine
- Supposed to be used with https://github.com/Lunran/sts_cli


# Prerequisites

- Ubuntu 18.04.5 LTS


# How to setup

- Get source codes
  - $ git clone https://github.com/Lunran/chitchat_api.git
  - $ cd chitchat_api
- Install modules
  - $ python3 -m venv venv
  - $ . venv/bin/activate
  - $ pip install --upgrade pip
  - $ pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
  - $ pip install -r requirements.txt


# How to use

- $ python main.py
- $ python test.py
