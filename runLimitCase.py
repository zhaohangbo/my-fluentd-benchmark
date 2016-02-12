#!/usr/bin/python
import sys
import time
import subprocess
import os

n_per_sec =str(1)
#b_per_msg =str(99999999)
b_per_msg =str(19999999)

list_post_cases=[
'./postMetrics.py -n 1 -b '+ b_per_msg,
'./postMetrics.py -n 1 -b '+ b_per_msg,
'./postMetrics.py -n 1 -b '+ b_per_msg,
'./postMetrics.py -n '+ b_per_msg +' -b -1  ',
'./postMetrics.py -n '+ b_per_msg +' -b -1  ',
'./postMetrics.py -n '+ b_per_msg +' -b -1  '
]

list_record_cases=[
'./callRecordSubprocess.py -n 1 -b '+ b_per_msg,
'./callRecordSubprocess.py -n 1 -b '+ b_per_msg,
'./callRecordSubprocess.py -n 1 -b '+ b_per_msg,
'./callRecordSubprocess.py -n '+ b_per_msg +' -b -1  ',
'./callRecordSubprocess.py -n '+ b_per_msg +' -b -1  ',
'./callRecordSubprocess.py -n '+ b_per_msg +' -b -1  '
]

logdir='/var/log/td-agent/flow' # path to your log directory

def main():
  if len(sys.argv) <= 1:
    print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> with -j <json_content>")
    sys.exit(-1)

  if sys.argv[1] == '-as_agent':
      for cmd in list_post_cases:
          #5min
          subprocess.call(cmd, shell=True)
          #1min sleep
          time.sleep(60)
          
          logfiles = sorted([ f for f in os.listdir(logdir)])
          for i in range(0,30):
              print "Most recent log file = %s" % (logfiles[-1],)
          subprocess.call('./getTotalCounts.py -p '+ str(logfiles[-1]) + '-as_agent', shell=True)
  elif sys.argv[1] == '-as_receiver':
      for cmd in list_record_cases:
          #5min
          subprocess.call(cmd, shell= True)
          #1min sleep
          time.sleep(60)
          
          logfiles = sorted([ f for f in os.listdir(logdir)])
          for i in range(0,30):
              print "Most recent log file = %s" % (logfiles[-1],)
          subprocess.call('./getTotalCounts.py -p '+ str(logfiles[-1]) + '-as_receiver', shell= True)
  else:
      print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> with -j <json_content>")
      sys.exit(-1)

if __name__ == "__main__":
  main()
