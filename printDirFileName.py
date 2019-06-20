#!/usr/bin/python
import sys

P1="total"
P2 = "./"
P3 = ".."

def process(argv):
    print "hello world; building names"
    fdata = open(argv[1],"r")
    print argv[1], " opened";
    pfx = '0';
    for line in fdata:
        if P2 in line:
                pfx = line[line.find(P2):-2];
            #    print pfx.strip()
        else:
          if P1 not in line:
            last= line.rfind(' ')
            name = line[last:]
            if (pfx != '0') & (name.strip() != ''):
                print "   ",pfx.rstrip()+'/'+ name.strip()


if __name__=="__main__":
    process(sys.argv)

