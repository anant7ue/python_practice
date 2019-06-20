#!/usr/bin/python

import os
import sys

TRUE = 1
FALSE = 0
SPACE = " "
NEWL = "\n"

def pushbuf(dfile, buf, residual):
    while (len(buf)>80):
        pos = buf.rfind(SPACE, 1, 80)
        print buf[:pos]
        dfile.write(buf[:pos] + NEWL)
        buf = buf[pos:]
    if(residual):
        print buf
        dfile.write(buf + NEWL + NEWL)
        return ""
    return buf

def process(filename):
  print filename
  srcfile = open(filename, "r")
  destfile = open(filename+"-fmt.out", "w")
  newpara = TRUE
  line1 = ""
  line2 = ""
  while 1:
    if(newpara):
        line1 = srcfile.next()
        line1 = line1.strip()
    line2 = srcfile.next()
    line2 = line2.strip()
    if len(line2) == 0:
        line1 = pushbuf(destfile, line1, TRUE)
        print len(line1), len(line2), "lens should be 0"
        newpara = TRUE
    else:
        line1 = line1 + SPACE + line2
        line2 = ""
        line1 = pushbuf(destfile, line1, FALSE)
        print len(line1), len(line2), "len2 should be 0; len1 probably not"
        newpara = FALSE


def main(argv):
  print(argv)
  if(len(argv) == 1):
    print "Usage: scriptname filename"
  else:
    process(argv[1])

if __name__ == "__main__":
   main(sys.argv)
