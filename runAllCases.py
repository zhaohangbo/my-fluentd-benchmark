#!/usr/bin/python
import sys
import time
import subprocess
import os

list_post_cases=[
#'./postMetrics.py   -r 50000',
#"""./postMetrics.py  -n 5000 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """,

#'./postMetrics.py  -n 5000 -json_metric_sample ',
#'./postMetrics.py  -n 5000 -json_log_sample ',
#'./postMetrics.py  -n 10000 -json_metric_sample ',
#'./postMetrics.py  -n 10000 -json_log_sample ',
#'./postMetrics.py  -n 15000 -json_metric_sample ',
#'./postMetrics.py  -n 15000 -json_log_sample '
]
for t in range(1,101):
    n_per_sec = t * 5000
    list_post_cases.append('./postMetrics.py -n ' + str(n_per_sec) +' -json_metric_sample')
    list_post_cases.append('./postMetrics.py -n ' + str(n_per_sec) +' -json_log_sample')

list_record_cases=[
#'./callRecordSubprocess.py -r 50000',
#'./callRecordSubprocess.py -n 5000'
]
for t in range(1,101):
    n_per_sec = t * 5000
    list_record_cases.append('./callRecordSubprocess.py -n '+ str(n_per_sec))
    list_record_cases.append('./callRecordSubprocess.py -n '+ str(n_per_sec))

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
          print "Most recent file = %s" % (logfiles[-1],)
          subprocess.call('./getTotalCounts.py -p '+ str(logfiles[-1]) + '-as_agent', shell=True)
  elif sys.argv[1] == '-as_receiver':
      for cmd in list_record_cases:
          #5min
          subprocess.call(cmd, shell= True)
          #1min sleep
          time.sleep(60)
          
          logfiles = sorted([ f for f in os.listdir(logdir)])
          print "Most recent file = %s" % (logfiles[-1],)
          subprocess.call('./getTotalCounts.py -p '+ str(logfiles[-1]) + '-as_receiver', shell= True)
  else:
      print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> with -j <json_content>")
      sys.exit(-1)

if __name__ == "__main__":
  main()
