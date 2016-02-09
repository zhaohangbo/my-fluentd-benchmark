#!/usr/bin/python
import subprocess
import time
import os
import errno


path ='/var/log/td-agent/test_results/'

iostat_file='iostat.log'
iostat_cmd="iostat -dkxt 1 >> '/var/log/td-agent/test_results/iostat.log'  &"
iostat_kill="pkill -f 'iostat -dkxt 1'"




#shell=True
#If passing a single string, either shell must be True or else the string must simply name the program to be executed without specifying any arguments.
subprocess.call(iostat_cmd,shell=True)
