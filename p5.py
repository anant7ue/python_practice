#!/usr/bin/python

import os
import sys
import csv


def check(filename, writer):
    datafile = open(filename.rstrip(), 'r')
    err_str="VCM_LOG_ERRO"
    endStr=");"
    linenum=0
    for line in datafile:
        errLog=""
        log=""
        linenum += 1
        if err_str in line:
            if endStr in line:
                errLog=":" + str(linenum) + ":" + line.strip()
                log=line.strip()
                #print filename.rstrip() + ":" + str(linenum) + ":" + line.strip()
            else:
                errLog=":" + str(linenum) + ":" + line.strip()
                log=line.strip()
                for count in range(1,15):
                    linenum += 1
                    line=datafile.next()
                    errLog=errLog+line.strip()
                    log=log+line.strip()
                    if endStr in line:
                        break;
        if len(errLog) > 0:
            writer.writerow({'filename':filename.rstrip(), 'lno':str(linenum), 'log':log, 'B':"", 'C':"", 'D':"", 'F':"", 'G':"", 'desc':"", 'pm-comment':""})
#            print filename.rstrip() + errLog


def main(argv):
#    cmd="""find . -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" > files.out"""
#    os.system(cmd)
    filelist=open(argv[1], 'r')
    csvFileName="csv/errorLog-"+argv[1]+".csv"
    csvFile=open(csvFileName,'w+')
    fieldnames = ['filename', 'lno', 'log', 'B', 'C', 'D', 'F', 'G','desc', 'pm-comment']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter='@')
    writer.writerow({'filename':'Log message ', 'lno':'', 'log':'', 'B':'Grammar, More info', 'C':'Warn-Level or delete', 'D':'Owner', 'F':'Handling Action needed', 'G':'Target release', 'desc':'', 'pm-comment':''})
    writer.writerow({'filename':"", 'lno':"", 'log':"", 'B':"", 'C':"", 'D':"", 'F':"", 'G':"", 'desc':"", 'pm-comment':""})
    for line in filelist:
        check(line, writer)


if __name__ == "__main__":
    main(sys.argv)
