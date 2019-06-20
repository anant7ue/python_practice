#! /usr/bin/python

import os
import sys
import string

NEW_LOG_LENGTH = 10;
PATTERN_LENGTH = 12;

def reformat(line, numcode, linenum):
    newstr = line
    err_str="VCM_LOG_ERRO"
    new_log_pfx="LOGG_ERROR"
    arg_spec_sym = "%"
    index = line.find(err_str)
    logStr = line.replace(err_str, new_log_pfx);
    newLogStr = logStr[:index+NEW_LOG_LENGTH+1]
    (newSpecStr, count) = reformatSpec(line[index+PATTERN_LENGTH+1:], 0, linenum);
    outline = newLogStr + newSpecStr 
    return (outline,count) 

def addhdr(filename ):
    destfile = open(filename.rstrip(), 'w')
    srcfile = open("../../be-not-fsm/"+filename.rstrip() , 'r')
    print filename 
    new_hdr80 ="/*----------------------------------------------------------------------------*\n" \
               " *                                                                            *\n" \
               " *     Copyright (c) 2016-2017 by Brocade Communications Systems, Inc. All    *\n" \
               " *     Rights Reserved.                                                       *\n" \
               " *                                                                            *\n" \
               " *     This software is licensed, and not freely redistributable. See the     *\n" \
               " *     license agreement for details.                                         *\n" \
               " *                                                                            *\n" \
               " *----------------------------------------------------------------------------*/\n\n"
    destfile.write(new_hdr80)
    for line in srcfile:
                destfile.write(line)
    srcfile.close()
    destfile.close()
    return 

def process(filename ):
#    destfile = open("../../"+filename.rstrip()+"1", 'w+')
    destfile = open(filename.rstrip(), 'w')
#    destfile = open("../../cprtchk", 'w+')
    srcfile = open("../../be-not-fsm/"+filename.rstrip() , 'r')
#    srcfile = open(filename.rstrip() , 'r')
    print filename 
    code_start1 = "ifdef"
    code_start2 = "define"
#    hdr_str="@date"
    hdr_str="2012-2013"
    hdr_str67="2016-2017"
    hdr_str_found = 0
    new_hdr_added = 0
    new_hdr81 =" *     Copyright (c) 2016-2017 by Brocade Communications Systems, Inc. All     *\n" \
               " *     Rights Reserved.                                                        *\n" \
               " *                                                                             *\n" \
               " *     This software is licensed, and not freely redistributable. See the      *\n" \
               " *     license agreement for details.                                          *\n" \
               " *                                                                             *\n"
    new_hdr80 =" *     Copyright (c) 2016-2017 by Brocade Communications Systems, Inc. All    *\n" \
              " *     Rights Reserved.                                                       *\n" \
              " *                                                                            *\n" \
              " *     This software is licensed, and not freely redistributable. See the     *\n" \
              " *     license agreement for details.                                         *\n" \
              " *                                                                            *\n"
    new_hdr_added = 0
    comma_newline=",\n"
    for line in srcfile:
        if (new_hdr_added == 0): 
#            if (hdr_str_found == 0) and (hdr_str not in line):
            if ((code_start1 in line) or (code_start2 in line)):
                print filename.rstrip(), "-- code precedes header -- errrr"
            if (hdr_str not in line):
                if (hdr_str67 in line):
                    print "len of new (c) hdr = ", len(line)
                destfile.write(line)
                continue
            else:
                if (len(line) == 81): 
                    destfile.write(new_hdr81)
                else:
                    destfile.write(new_hdr80)
                print "len of (c) hdr = ", len(line)
                destfile.write(line)
                new_hdr_added = 1
        else:
            destfile.write(line)
    if (new_hdr_added == 0): 
        print filename.rstrip(), " -- file missing header -- errrr"
    srcfile.close()
    destfile.close()
    return 

def bkslash_end(filename):
    srcfile = open(filename.rstrip() , 'r')
    count = 0
    err_str="VCM_LOG_ERRO"
    endStr=");"
    fmt = "\\"
    print filename.rstrip()
    for line in srcfile:
        if err_str in line:
            if fmt in line:
#                print line
                count+= 1 
            while endStr not in line:
                line = srcfile.next()
                if fmt in line:
#                    print line
                    count+= 1
    return count

def whichhdr(filename ):
    return
def main(argv):
#    cmd="""find . -name "*.c" -o -name "*.cpp" > files-src.out"""
#    os.system(cmd)
#    filelist=open("files-be_nofsm.txt", 'r')
#    filelist=open("files-fsm-missing-hdr.txt", 'r')
    filelist=open("files-be-nofsm-missing-cprt-hdr", 'r')
    for filename in filelist:
        print filename
        addhdr(filename)
#        process(filename)
#        whichhdr(filename)

if __name__ == "__main__":
    main(sys.argv)
