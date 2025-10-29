#!/bin/bash
sudo apt-get update -y
sudo apt-get install ruby-full -y
sudo apt-get install wget -y 
cd /home/ubuntu
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
sudo chmod +x ./install
sudo ./install auto
sudo systemctl enable codedeploy-agent
sudo systemctl start codedeploy-agent