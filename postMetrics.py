#!/usr/bin/python
import requests
import json
import sys
import time
import os
import errno
import datetime
import subprocess
messages_per_sec= 100 #  messages/sec   how many messages you sent per second


url = "http://10.10.10.11:8888/collectd"
data = {'sender': 'Hangbo_Metrics'}
data2= {"names": ["J.J.", "April"], "years": [25, 29]}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
def getLenInUtf8(s):
    return len(s.encode('utf-8'))
def getSizeInBytes(s):
    return sys.getsizeof(s)
def printResults(msg_len_in_utf8,msg_size_in_bytes,respon):
    print('jutf8_len: ',msg_len_in_utf8)
    print('size of object in bytes', msg_size_in_bytes)
    print('respon',respon)

one_hundred_byte_msg='Two roads diverged in a wood, and I took the one less traveled.'
one_kb_msg = one_hundred_byte_msg*15+'Two roads diverged in a wood, and I took t'
one_mb_msg = one_kb_msg * 1024+ one_kb_msg*38+'Two roads diverged in a wood,.' + 'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'
#print('one_hundred_byte_msg',getSizeInBytes(one_hundred_byte_msg))
#print('one_kb_msg',getSizeInBytes(one_kb_msg))
#print('one_mb_msg',getSizeInBytes(one_mb_msg))  #1M = 1024* (1024bytes) = 1048576 bytes'Two roads diverged in a wood, and I took the one less traveled.'


RATE_INPUT = 'no input'       # -r <bytes/seconds>
Num_INPUT  = 'no input'       # -n <numbersOfMsg/second>




def get_msg_of_specific_bytes(bytes_per_second):
    msg =''
    bytes_per_second = int(bytes_per_second)
    diff = bytes_per_second - sys.getsizeof(msg)
    while(diff>0):
        if diff < 100:
            msg = msg + 's'
        elif diff < 200:
            msg =msg +'small.'
        elif diff < 500:      #  100 <diff < 500
            msg = msg +  'larger....'
        elif diff < 1024:     #  500 <diff < 1K
            msg = msg + one_hundred_byte_msg
        elif diff < 1048576:  #  1K  <diff < 1M
            msg = msg + one_kb_msg
        else:                 #       diff >=1M
            msg = msg + one_mb_msg
        diff = bytes_per_second - sys.getsizeof(msg)
    return msg

def post_metrics_bytes_per_second(bytes_per_second, msg_of_specific_bytes):
    a_dict = {"msg":msg_of_specific_bytes}
    data.update(a_dict)
    json_str =json.dumps(data)
    msg_len_in_utf8 = getLenInUtf8(json_str)
    msg_size_in_bytes= getSizeInBytes(json_str) #Return the size of object in bytes.
    respon = requests.post(url, data=json_str, headers=headers)
    printResults(msg_len_in_utf8,msg_size_in_bytes,respon)
    time.sleep(1)  # sleep 1 second

def post_metrics_numbers_per_second(numbers_per_second, intput_json_data):
    if intput_json_data is None:
        intput_json_data= data
    time1 = datetime.datetime.now()
    for i in range(0,numbers_per_second):
        json_str =json.dumps(intput_json_data)
        msg_len_in_utf8 = getLenInUtf8(json_str)
        msg_size_in_bytes= getSizeInBytes(json_str) #Return the size of object in bytes.
        respon = requests.post(url, data=json_str , headers=headers)
        printResults(msg_len_in_utf8,msg_size_in_bytes,respon)

    time2  = datetime.datetime.now()
    time_passed = time2 - time1
    ms_left = (1000-time_passed.total_seconds())
    print ('ms_left :',ms_left,' ms')
    if ms_left > 0:
        time.sleep(ms_left/1000.0)
    else:
        print('can not post'+numbers_per_second+'in 1 seconds , totally needs'+ str(1-ms_left/1000.0)+'seconds')

path ='/var/log/td-agent/perf_results/'

iostat_file='iostat.log'
iostat_cmd='iostat -dkxt 1 >> '+path+iostat_file+' &'
iostat_kill="pkill -f 'iostat -dkxt 1'"

vmstat_file='vmstat.log'
vmstat_cmd ='vmstat 1 >> '+path+vmstat_file+' &'
vmstat_kill="pkill -f 'vmstat 1'"

dstat_file='dstat.log'
dstat_cmd ='dstat >> '+path+dstat_file+' &'
dstat_kill="pkill -f 'dstat'"

free_file='free.log'
free_cmd ='free >> '+path+free_file+' &'
free_kill="pkill -f  'free'"

top_file='top.log'
top_cmd ='top -c >> '+path+top_file+' &'
top_kill="pkill -f  'top -c'"

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def touchFiles(bytes_per_second , postfix):
    bytes_per_second = str(bytes_per_second)
    postfix = str(postfix)
    if not os.path.isfile(path + iostat_file + bytes_per_second + postfix):
        open(path+iostat_file + bytes_per_second + postfix, "a+").close()
    if not os.path.isfile(path+vmstat_file + bytes_per_second + postfix):
        open(path+vmstat_file + bytes_per_second + postfix, "a+").close()
    if not os.path.isfile(path+dstat_file + bytes_per_second + postfix):
        open(path+dstat_file + bytes_per_second + postfix, "a+").close()
    if not os.path.isfile(path+free_file + bytes_per_second + postfix):
        open(path+free_file + bytes_per_second + postfix, "a+").close()
    if not os.path.isfile(path+top_file + bytes_per_second + postfix):
        open(path+top_file + bytes_per_second + postfix, "a+").close()

def form_cmd_r(bytes_per_second):
    bytes_per_second=str(bytes_per_second)
    global iostat_cmd
    iostat_cmd='iostat -dkxt 1 >> ' + path + iostat_file + bytes_per_second+'_r_' +' &'
    global vmstat_cmd
    vmstat_cmd ='vmstat 1 >> ' + path + vmstat_file + bytes_per_second +'_r_' +' &'
    global dstat_cmd
    dstat_cmd ='dstat >> ' + path + dstat_file + bytes_per_second +'_r_' +' &'
    global free_cmd
    free_cmd ='free >> ' + path+free_file + bytes_per_second +'_r_' +' &'
    global top_cmd
    top_cmd ='top -c >> '+ path + top_file + bytes_per_second +'_r_' +' &'

def form_cmd_n(bytes_per_second):
    bytes_per_second=str(bytes_per_second)
    global iostat_cmd
    iostat_cmd='iostat -dkxt 1 >> ' + path + iostat_file + bytes_per_second+'_n_' +' &'
    global vmstat_cmd
    vmstat_cmd ='vmstat 1 >> ' + path + vmstat_file + bytes_per_second +'_n_' +' &'
    global dstat_cmd
    dstat_cmd ='dstat >> ' + path + dstat_file + bytes_per_second +'_n_' +' &'
    global free_cmd
    free_cmd ='free >> ' + path+free_file + bytes_per_second +'_n_' +' &'
    global top_cmd
    top_cmd ='top -c >> '+ path + top_file + bytes_per_second +'_n_' +' &'

def record_sys_status_to_log_r(bytes_per_second):
    bytes_per_second = str(bytes_per_second)
    mkdir_p(path)
    touchFiles(bytes_per_second,'_r_')
    form_cmd_r(bytes_per_second)
    print(iostat_cmd,vmstat_cmd,dstat_cmd,free_cmd)
    subprocess.call(iostat_cmd, shell=True)
    subprocess.call(vmstat_cmd, shell=True)
    subprocess.call(dstat_cmd, shell=True)
    subprocess.call(free_cmd, shell=True)
    #subprocess.call(top_cmd, shell=True)

def record_sys_status_to_log_n(bytes_per_second):
    bytes_per_second = str(bytes_per_second)
    mkdir_p(path)
    touchFiles(bytes_per_second,'_n_')
    form_cmd_n(bytes_per_second)
    print(iostat_cmd,vmstat_cmd,dstat_cmd,free_cmd)
    subprocess.call(iostat_cmd, shell=True)
    subprocess.call(vmstat_cmd, shell=True)
    subprocess.call(dstat_cmd, shell=True)
    subprocess.call(free_cmd, shell=True)
    #subprocess.call(top_cmd, shell=True)

def kill_recording_process():
    subprocess.call(iostat_kill, shell=True)
    subprocess.call(vmstat_kill, shell=True)
    subprocess.call(dstat_kill, shell=True)
    subprocess.call(free_kill, shell=True)
    #subprocess.call(top_kill, shell=True)

def main():
  if len(sys.argv) <= 1:
    print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> with -j <json_content>")
    sys.exit(-1)

  if sys.argv[1] == '-r':
      bytes_per_second =int(sys.argv[2])
      msg_of_specific_bytes = get_msg_of_specific_bytes(bytes_per_second)

      record_sys_status_to_log_r(bytes_per_second)
      begin_time   = time.time()
      exec_time_left=time.time() - begin_time

      while exec_time_left < 300:
         post_metrics_bytes_per_second(bytes_per_second,msg_of_specific_bytes)
	 exec_time_left= time.time() - begin_time
         print('exec_time_left:',exec_time_left)
      kill_recording_process()

  elif sys.argv[1] == '-n':
      numbers_per_second =int(sys.argv[2])
      j_content = None
      if len(sys.argv) >=4:
          print " get in len(sys.argv) >=4:  "
          if len(sys.argv)==4:
              print('missing json content to input')
          elif sys.argv[3]=='-json' and len(sys.argv)==5:
              #j_content = json.dumps(sys.argv[4])  wrong
              j_content = json.loads(sys.argv[4])  # use loads
              print('j_content  : ', j_content)
          else:
              print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> or -j <json_content>")

      record_sys_status_to_log_n(numbers_per_second)
      begin_time   = time.time()
      exec_time_left=time.time() - begin_time
      #Run 5 mins
      while exec_time_left < 300:
          post_metrics_numbers_per_second(numbers_per_second, j_content)
	  exec_time_left= time.time() - begin_time
	  print('exec_time_left:',exec_time_left)
      kill_recording_process()


if __name__ == "__main__":
  main()
