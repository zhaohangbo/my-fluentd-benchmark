#!/usr/bin/python
import requests
import json
import sys
import time
import os
import errno
import datetime
import subprocess
import random
import threading
import multiprocessing
url = "http://10.10.10.11:8888/collectd"
#url = "http://10.0.0.98:8888/collectd"

numbers_per_second=500
metric_base={"a":"a"}

metric_sample= {
    "values": [1934546],
    "dstypes": ["derive"],
    "dsnames": ["value"],
    "interval": 10,
    "host": "zookeeper-2.zeus-test.va1.ciscozeus.io..",
    "plugin": "cpu",
    "plugin_instance": "0",
    "type": "cpu",
    "type_instance": "wait",
    "timestamp": "2016-02-10 21:41:07 +0000",
    "in_time": "2016-02-10 21:41:07 +0000",
    "tag": "metrics.collectd.randomuser-internal_token"
}
log_sample={
    "host": "postgres-1",
    "ident": "CRON",
    "pid": "31459,",
    "message": "pam_unix(cron:session): session opened for user postgres by (uid=0)",
    "timestamp": "2016-02-10 21:41:01 +0000",
    "in_time": "2016-02-10 21:41:01 +0000",
    "tag": "logs.syslog.authpriv.info.randomuser-internal_token"
}



headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
def getLenInUtf8(s):
    return len(s.encode('utf-8'))
def getSizeInBytes(s):
    return sys.getsizeof(s)
def printResults(msg_len_in_utf8,msg_size_in_bytes,respon):
    if msg_len_in_utf8!=None:
        print('jutf8_len: ',msg_len_in_utf8)
    if msg_size_in_bytes!=None:
        print('size of object in bytes', msg_size_in_bytes)
    if respon!=None:
        print('respon',respon)

one_hundred_byte_msg='Two roads diverged in a wood, and I took the one less traveled.'
one_kb_msg = one_hundred_byte_msg*15+'Two roads diverged in a wood, and I took t'
one_mb_msg = one_kb_msg * 1024+ one_kb_msg*38+'Two roads diverged in a wood,.' + 'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'+'Two roads diverged in a wood, and I took the one less traveled.'
#print('one_hundred_byte_msg',getSizeInBytes(one_hundred_byte_msg))
#print('one_kb_msg',getSizeInBytes(one_kb_msg))
#print('one_mb_msg',getSizeInBytes(one_mb_msg))  #1M = 1024* (1024bytes) = 1048576 bytes'Two roads diverged in a wood, and I took the one less traveled.'


RATE_INPUT = 'no input'       # -r <bytes/seconds>
Num_INPUT  = 'no input'       # -n <numbersOfMsg/second>

def get_zero_or_one():
    if bool(random.getrandbits(1)) == True:
        return 1
    else:
        return 0

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

def post_metrics_n_b(numbers_per_second, j_str_of_specific_bytes):
    time1 = datetime.datetime.now()
    for i in range(0,numbers_per_second):
        msg_size_in_bytes= getSizeInBytes(j_str_of_specific_bytes) #Return the size of object in bytes.
        respon = requests.post(url, data=j_str_of_specific_bytes , headers=headers)
        printResults(None,msg_size_in_bytes,respon)
        print('posted ',i,'times')

    time2  = datetime.datetime.now()
    time_passed = time2 - time1
    ms_left = (1000-time_passed.total_seconds()*1000)
    print ('ms_left :',ms_left,' ms')
    if ms_left > 0:
        time.sleep(ms_left/1000.0)
    else:
        print('can not post'+numbers_per_second+'in 1 seconds , totally needs'+ str(1-ms_left/1000.0)+'seconds')

def post_metrics_bytes_per_second( j_str):
    msg_len_in_utf8 = getLenInUtf8(j_str)
    msg_size_in_bytes= getSizeInBytes(j_str) #Return the size of object in bytes.
    respon = requests.post(url, data=j_str, headers=headers)
    printResults(msg_len_in_utf8,msg_size_in_bytes,respon)
    time.sleep(1)  # sleep 1 second

def post_metrics_numbers_per_second(numbers_per_second, json_str):
    time1 = datetime.datetime.now()
    for i in range(0 ,numbers_per_second):
        msg_len_in_utf8 = getLenInUtf8(json_str)
        msg_size_in_bytes= getSizeInBytes(json_str) #Return the size of object in bytes.
        respon = requests.post(url, data=json_str , headers=headers)
        printResults(msg_len_in_utf8,msg_size_in_bytes,respon)
        print('posted ',i,'times')

    time2  = datetime.datetime.now()
    time_passed = time2 - time1
    ms_left = (1000-time_passed.total_seconds()*1000)
    print ('ms_left :',ms_left,' ms')
    if ms_left > 0:
        time.sleep(ms_left/1000.0)
    else:
        print('can not post'+str(numbers_per_second)+'in 1 seconds , totally needs'+ str(1-ms_left/1000.0)+'seconds')

#def post_metrics_numbers_per_second(numbers_per_second, intput_json_data):
#    if intput_json_data is None:
#        intput_json_data= data
#    time1 = datetime.datetime.now()
#    times_of_thousands = int(numbers_per_second/1000)
#    for i in range(0, numbers_per_second):
#        try:
#                for j in range(0,1000):
#                        json_str =json.dumps(intput_json_data)
#                        msg_len_in_utf8 = getLenInUtf8(json_str)
#                        msg_size_in_bytes= getSizeInBytes(json_str) #Return the size of object in bytes.
#                        respon = requests.post(url, data=json_str , headers=headers)
#                        printResults(msg_len_in_utf8,msg_size_in_bytes,respon)
#        except requests.exceptions.ConnectionError:
#                print("No connection could be made because the target machine actively refused it")
#                time.sleep(0.5)
#                pass
#        time.sleep(2/1000.0)
#    time2  = datetime.datetime.now()
#    time_passed = time2 - time1
#    ms_left = (1000-time_passed.total_seconds()*1000)
#    print ('ms_left :',ms_left,' ms')
#    if ms_left > 0:
#        time.sleep(ms_left/1000.0)
#    else:
#        print('can not post'+numbers_per_second+'in 1 seconds , totally needs'+ str(1-ms_left/1000.0)+'seconds')

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

def touchFiles(prefix , postfix):
    prefix = str(prefix)
    postfix = str(postfix)
    if not os.path.isfile(path + iostat_file + prefix + postfix):
        open(path+iostat_file + prefix + postfix, "a+").close()
    if not os.path.isfile(path+vmstat_file + prefix + postfix):
        open(path+vmstat_file + prefix + postfix, "a+").close()
    if not os.path.isfile(path+dstat_file + prefix + postfix):
        open(path+dstat_file + prefix + postfix, "a+").close()
    if not os.path.isfile(path+free_file + prefix + postfix):
        open(path+free_file + prefix + postfix, "a+").close()
    if not os.path.isfile(path+top_file + prefix + postfix):
        open(path+top_file + prefix + postfix, "a+").close()

def form_cmd (prefix,postfix):
    prefix=str(prefix)
    postfix=str(postfix)
    global iostat_cmd
    iostat_cmd='iostat -dkxt 1 >> ' + path + iostat_file + prefix+postfix +' &'
    global vmstat_cmd
    vmstat_cmd ='vmstat 1 >> ' + path + vmstat_file + prefix +postfix +' &'
    global dstat_cmd
    dstat_cmd ='dstat >> ' + path + dstat_file + prefix +postfix +' &'
    global free_cmd
    free_cmd ='free >> ' + path+free_file + prefix +postfix +' &'
    global top_cmd
    top_cmd ='top -c >> '+ path + top_file + prefix +postfix +' &'

def record_sys_status_to_log( prefix , postfix):
    mkdir_p(path)
    touchFiles(prefix, postfix)
    form_cmd(prefix, postfix)
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


class myPostThread (threading.Thread):
    def __init__(self, threadID, name, numbers_per_second,json_str, flag):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.numbers_per_second= numbers_per_second
        self.json_str=json_str
        self.flag=flag
    def run(self):
        print "Starting " + self.name
        if self.flag =='_n_':
            post_metrics_numbers_per_second(self.numbers_per_second, self.json_str)
        elif self.flag=='_r_':
            pass
        elif self.flag=='_n_b_':
            pass
        else:
            pass
        print "Exiting " + self.name

def createThread( n ,numbers_per_second,json_str,flag ):
    for i in range(0,n):
        myPostThread(i, "Thread-"+str(i), numbers_per_second,json_str,flag).start()

def multiProcess( n ,numbers_per_second,json_str ):
    for i in range(0,n):
        p = multiprocessing.Process(target=post_metrics_numbers_per_second, args=(numbers_per_second,json_str,))
        p.start()

def main():
  if len(sys.argv) <= 1:
    print("Usage: postMetrics -n <numbersOfMsg/second> and -b <bytes/msg> ")
    print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> with -j <json_content>")
    sys.exit(-1)

  if sys.argv[1] == '-n' and sys.argv[3] == '-b':
      numbers_per_second =int(sys.argv[2])
      bytes_per_msg      =int(sys.argv[4])
      if bytes_per_msg>0:
          msg_of_specific_bytes = get_msg_of_specific_bytes(bytes_per_msg)
          metric_base.update({"msg":msg_of_specific_bytes})
      else:
          #bytes_per_msg<0 use default min metric_base
          pass

      j_str_of_specific_bytes =json.dumps(metric_base)

      record_sys_status_to_log( str(numbers_per_second)+'_'+str(bytes_per_msg) , '_n_b_')
      begin_time   = time.time()
      exec_time_left=time.time() - begin_time

      while exec_time_left < 300:
         post_metrics_n_b( numbers_per_second, j_str_of_specific_bytes)

      exec_time_left= time.time() - begin_time
      print('exec_time_left:',exec_time_left)
      kill_recording_process()

  if sys.argv[1] == '-r':
      bytes_per_second =int(sys.argv[2])
      msg_of_specific_bytes = get_msg_of_specific_bytes(bytes_per_second)
      metric_base.update({"msg":msg_of_specific_bytes})
      j_str_of_specific_bytes =json.dumps(metric_base)
      record_sys_status_to_log( str(bytes_per_second) , '_b_')

      begin_time   = time.time()
      exec_time_left=time.time() - begin_time

      while exec_time_left < 300:
         post_metrics_bytes_per_second( j_str_of_specific_bytes)
         exec_time_left= time.time() - begin_time
         print('exec_time_left:',exec_time_left)
      kill_recording_process()

  elif sys.argv[1] == '-n':
      numbers_per_second =int(sys.argv[2])
      intput_json = None
      if len(sys.argv) >=4:
          print " get in len(sys.argv) >=4:  "
          if len(sys.argv)==4:
              if str(sys.argv[3])=='-json_metric_sample':
                  intput_json = metric_sample
              elif str(sys.argv[3])=='-json_log_sample':
                  intput_json = log_sample
              else:
                  print('missing json content to input')
          elif sys.argv[3]=='-json' and len(sys.argv)==5:
              intput_json = json.loads(sys.argv[4])  # use loads
              print('j_content  : ', intput_json)
          else:
              print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> or -j <json_content>")

      record_sys_status_to_log( str(numbers_per_second) , '_n_')
      if intput_json is None:
          print('intput_json_data is none!!!',intput_json,'Use default json data')
          intput_json= metric_base
      json_str =json.dumps(intput_json)
      begin_time   = time.time()
      exec_time_left=time.time() - begin_time

      # Create new threads
      #createThread( 10 ,numbers_per_second,json_str,'_n_')
      #time.sleep(60)
      #createThread( 10 ,numbers_per_second,json_str,'_n_')
      #time.sleep(60)
      #createThread( 10 ,numbers_per_second,json_str,'_n_')

      #multiProcess( 10 ,numbers_per_second,json_str )

      #Run 5 mins
      while exec_time_left < 300:
          post_metrics_numbers_per_second(numbers_per_second, json_str)
          exec_time_left= time.time() - begin_time
          print('exec_time_left---exec_time_left---exec_time_left : ', exec_time_left)

      kill_recording_process()


if __name__ == "__main__":
  main()
