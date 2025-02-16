#!/bin/bash

read -p "The address of the input data to be read: " input_folder
read -p "The address where the input data is stored: " output_folder

python3 evaluation/Multi_Round_DSR.py $input_folder $output_folder