#!/usr/bin/python
import sys
import time
import subprocess


list_post_cases=[
'./postMetrics.py   -r 3000',
'./postMetrics.py   -r 4000',
'./postMetrics.py   -r 10000',
'./postMetrics.py   -r 20000',
'./postMetrics.py   -r 30000',
'./postMetrics.py   -r 40000',
'./postMetrics.py   -r 50000',

 """./postMetrics.py  -n 500 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """,
 """./postMetrics.py  -n 1000 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """,
 """./postMetrics.py  -n 1500 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """,
 """./postMetrics.py  -n 2000 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """,
 """./postMetrics.py  -n 3000 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """,
 """./postMetrics.py  -n 4000 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """,
 """./postMetrics.py  -n 5000 -json '{"names": ["J.J.", "April"], "years": [25, 29]}' """
]

list_record_cases=[
'./callRecordSubprocess.py -r 3000',
'./callRecordSubprocess.py -r 4000',
'./callRecordSubprocess.py -r 10000',
'./callRecordSubprocess.py -r 20000',
'./callRecordSubprocess.py -r 30000',
'./callRecordSubprocess.py -r 40000',
'./callRecordSubprocess.py -r 50000',

'./callRecordSubprocess.py -n 500',
'./callRecordSubprocess.py -n 1000',
'./callRecordSubprocess.py -n 1500',
'./callRecordSubprocess.py -n 2000',
'./callRecordSubprocess.py -n 3000',
'./callRecordSubprocess.py -n 4000',
'./callRecordSubprocess.py -n 5000'
]
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
  elif sys.argv[1] == '-as_receiver':
      for cmd in list_record_cases:
          #5min
          subprocess.call(cmd, shell= True)
          #1min sleep
          time.sleep(60)
  else:
      print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> with -j <json_content>")
      sys.exit(-1)

if __name__ == "__main__":
  main()
