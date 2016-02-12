#!/usr/bin/python
import subprocess
import time
import os
import errno
import sys

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

def main():
    if len(sys.argv) <= 1:
	print("Usage: callRecordSubprocess -r <bytes/seconds> or -n <numbersOfMsg/second>")
	sys.exit(-1)

    if sys.argv[1] == '-n' and sys.argv[3] == '-b':
        numbers_per_second =int(sys.argv[2])
        bytes_per_second =int(sys.argv[4])
        record_sys_status_to_log(str(numbers_per_second)+'_'+str(bytes_per_second),'_n_b_')
    elif sys.argv[1]=='-r':
    	bytes_per_second =int(sys.argv[2])
    	record_sys_status_to_log(bytes_per_second,'_r_')
    elif sys.argv[1]=='-n':
    	numbers_per_second =int(sys.argv[2])
        record_sys_status_to_log(numbers_per_second,'_b_')
    else:
    	print("Usage: callRecordSubprocess -r <bytes/seconds> or -n <numbersOfMsg/second>")
    	sys.exit(-1)
    
    #Run 5 mins
    time.sleep(300)
    kill_recording_process()

if __name__ == "__main__":
  main()

