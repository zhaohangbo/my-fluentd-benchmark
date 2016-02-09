# Fluentd benchmark - forward

This benchmarks following architecture scenario:

```
  Agent Node                                        Receiver Node
  +---------------------------------------------+             +---------------------+
  | +---------------+      +-----------------+  |             |  +---------------+  |
  | |  	Python 	    |      |                 |  |             |  |               |  |
  | |	Script      +----->|     FluentD     +--------------->   |  FluentD      |  |
  | |  	Posts	    |      |                 |  |             |  |               |  |
  | +---------------+   in_http-------out_secure_forward  in_secure_forward------+  |
  +---------------------------------------------+             +---------------------+
```

## Agent==  (in_http —> FluentD —>out_secure_forward)

```
Agent Side: Two methods to post metrics to in_http
1.  postMetrics.py   -r 1000  ,(1000 bytes/sec)
2.  postMetrics.py  -n 10 -json '{"names": ["J.M.Zeus", “Hangbo"], "years": [25, 24]}'  ,(10 msgs/sec)
```
## Receiver= (in_secure_forward —> FluentD —>out_file)
```
Server Side: Two methods to record results 
1.  callRecordSubprocess.py -r 1000  ,(corresponding to 'postMetrics.py   -r 1000')
2.  callRecordSubprocess.py -n 10    ,(corresponding to 'postMetrics.py  -n 10 -json')
```
## Auto Test

Step 1: git clone this repository both on Agent and Receiver side

Step 2: Test Cases
```
list_record_cases in runAllCases.py
list_record_cases in runAllCases.py
```
Step 3: Auto Test Commands
```
On the agent    side: ./runAllCases.py -as_agent
On the receiver side: ./runAllCases.py -as_receiver
```


Step 4: Results Location
```
Correctness Records location:
  /var/log/td-agent/trafic.basic.*.log

Performance Records location:
  /var/log/td-agent/test_results/*
```


Step 5: Add Your Own Test Cases:
```
Change the cases in runAllCases.py.
For example, you’d like to test sending 10086 bytes/sec metrics from Agent to Receiver,
1.add case "./postMetrics.py   -r  10086” 
  to list_record_cases in runAllCases.py
2.add case "./callRecordSubprocess.py -r 10086”
  to list_record_cases in runAllCases.py
```


You may use linux commands `iostat -dkxt 1`, `vmstat 1`, `top -c`, `free`, or `dstat` to measure system resources. 

## Sample Result

This is a sample result running on my environement


Agent Machine Spec
```
CPU	  : Intel(R) Core(TM) i7-4850HQ CPU @ 2.30GHz
Memory:	2G
Disk	: 40G(10000rpm) x 2 [SAS-HDD]
OS    : Ubuntu 14.04.3 LTS	trusty
```

Receiver Machine Spec
```
CPU	  : Intel(R) Core(TM) i7-4850HQ CPU @ 2.30GHz
Memory:	1G
Disk	: 40G(10000rpm) x 2 [SAS-HDD]
OS    : Ubuntu 14.04.3 LTS	trusty
```

Result


|                             |                       | Agent   |             |         |
|-----------------------------|-----------------------|---------|-------------|---------|
| rate of writing (msgs/sec)  | reading (msgs/sec)    | CPU (%) | Memory (kB) | Remarks |
| 10                          | 10                    |         |             |         |
|                             |                       |         |             |         |
|                             |                       |         |             |         |
|                             |                       |         |             |         |
|                             |                       |         |             |         |
|                             |                       |         |             | MAX     |
|                             | N/A                   |         |             |         |
|                             | N/A                   |         |             |         |
|                             | N/A                   |         |             | MAX     |

