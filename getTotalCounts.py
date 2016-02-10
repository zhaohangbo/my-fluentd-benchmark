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
                count += int(line.split('"count":')[1].split(',')[0])
            if(sys.argv[3]=='-as_agent'):
                print("---------------- Totally sent " + str(count) + " messages ! ----------------")
                print("                                                                            ")
                f.write("                                                                            ")
                f.write("---------------- Totally sent " + str(count) + " messages ! ----------------")
                f.write("                                                                            ")
            elif(sys.argv[3]=='-as_receiver'):
                print("---------------- Totally received " + str(count) + " messages ! ----------------")
                print("                                                                            ")
                f.write("                                                                            ")
                f.write("---------------- Totally received " + str(count) + " messages ! ----------------")
                f.write("                                                                            ")

if __name__ == "__main__":
  main()
