#!/usr/bin/python
import sys
import os

#s= """2016-02-08T14:33:35-08:00	traffic.metrics	{"count":51,"bytes":152643,"count_rate":0.85,"bytes_rate":2544.05}"""
#cnt = s.split('"count":')[1].split(',')[0]
#print(cnt)

def main():
  if len(sys.argv) != 4:
    print("Usage: getTotalCounts  -p file_pith -as_agent or -as_receiver")
    sys.exit(-1)

  if sys.argv[1] == '-p':
      file_path = str(sys.argv[2])
      if os.path.isfile(file_path):
        with open(file_path,"a+") as f:
            count = 0
            for line in f:
                if "traffic.metrics" in line:
                    count += int(line.split('"count":')[1].split(',')[0])
                #elif line.startswith("-----"):
                #    count = 0
   		else:
		    pass
            if(sys.argv[3]=='-as_agent'):
                print("--------- Totally sent " + str(count) + " messages ! ---------")
                print("    \n")
                f.write("    \n")
                f.write("---------------- Totally sent " + str(count) + " messages ! ---------")
                f.write("    \n")
            elif(sys.argv[3]=='-as_receiver'):
                print("--------- Totally received " + str(count) + " messages ! ---------")
                print("    \n")
                f.write("    \n")
                f.write("--------- Totally received " + str(count) + " messages ! ---------")
                f.write("    \n")
            else:
                print("-as_agent or -as_receiver")
                print("Usage: getTotalCounts  -p file_pith -as_agent or -as_receiver")
                sys.exit(-1)
if __name__ == "__main__":
  main()
