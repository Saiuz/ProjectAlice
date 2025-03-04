#!/usr/bin/env bash

curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
apt-get update
apt-get install -y matrixio-creator-init libmatrixio-creator-hal libmatrixio-creator-hal-dev

sudo -u pi bash <<EOF
    /home/pi/snipsLedControl/venv/bin/pip3 --no-cache-dir install matrix-lite
EOF
