#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl enable bankapp.service
sudo systemctl start bankapp.service
