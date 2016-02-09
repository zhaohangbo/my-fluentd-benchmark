#!/usr/bin/python
import json
import sys
import time
import datetime

path = "/var/log/td-agent/my_log.log"

#data = {'sender': 'Hangbo_Metrics'}
#data2= {"names": ["J.J.", "April"], "years": [25, 29]}

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

def write_logs_bytes_per_second(bytes_per_second, msg_of_specific_bytes):
    print('... enter--> write_logs_bytes_per_second()')
    log_file = open(path, "w")
    log_file.write("time:"+ str(time.time()) +"msg_of_specific_bytes: %s" % msg_of_specific_bytes)
    log_file.close()
    time.sleep(1)  # sleep 1 second
    print('... leave--> write_logs_bytes_per_second()')

def write_logs_numbers_per_second( numbers_per_second, l_content):
    log_file = open(path, "w")
    #open and close file once every 30 seconds
    for times in range(0,30):
        print('... enter--> write_logs_numbers_per_second() 1 time')
        for i in range(numbers_per_second):
            log_file.write("time:"+ str(time.time()) +"l_content : %s" % l_content)
        time.sleep(1)  # sleep 1 second
        print('... leave--> write_logs_numbers_per_second() 1 time')
    log_file.close()


def printResults(msg_len_in_utf8,msg_size_in_bytes,respon):
    print('jutf8_len: ',msg_len_in_utf8)
    print('size of object in bytes', msg_size_in_bytes)
    print('respon',respon)

def main():
  if len(sys.argv) <= 1:
    print("Usage: writeLogs -r <bytes/seconds> or -n <numbersOfMsg/second> with -l <log_content>")
    sys.exit(-1)

  if sys.argv[1] == '-r':
      bytes_per_second =sys.argv[2]
      msg_of_specific_bytes = get_msg_of_specific_bytes(bytes_per_second)
      while True:
         write_logs_bytes_per_second(bytes_per_second,msg_of_specific_bytes)
  elif sys.argv[1] == '-n':
      numbers_per_second =int(sys.argv[2])
      l_content = None
      if len(sys.argv) >=4:
          print " get in len(sys.argv) >=4:  "
          if len(sys.argv)==4:
              print('missing json content to input')
          elif sys.argv[3]=='-log' and len(sys.argv)==5:
              l_content = str(sys.argv[4])
              print('j_content  : ', l_content)
          else:
              print("Usage: postMetrics -r <bytes/seconds> or -n <numbersOfMsg/second> or -j <json_content>")

      while True:
          write_logs_numbers_per_second(numbers_per_second, l_content)

if __name__ == "__main__":
  main()

