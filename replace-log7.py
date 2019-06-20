#! /usr/bin/python

import os
import sys
import string

NEW_LOG_LENGTH = 10;
PATTERN_LENGTH = 12;

def chk_line_end(line, astr_spec_mode):
    bkslash = "\\"
    dq_str="\""
    esc_dq="\\\""
    last_bkslash_idx = line.rfind(bkslash)
    val = 0
    if bkslash in line:
        if (line.count(dq_str) %2 != 0):
          if (line[last_bkslash_idx+1:].isspace()):
            val = 1
          else:     
            print " non-whitespace after bkslash -- must be escape-char -- return 0"
#    print "returning 0 for bkslash end"
    dq_count = line.count(dq_str)
    str_spec_mode = astr_spec_mode ^ ((dq_count-line.count(esc_dq))%2)
    print str_spec_mode

    return str_spec_mode

def print_imsi_str(filename, lineno):
    loggfile = open("../../imsi_str_log_list_mini", 'a')
    loggfile.write(filename.rstrip() )
    loggfile.write(" PRINTS_IMSI_AT ")
    loggfile.write(str(lineno) + "\n")
    loggfile.close()

def fetch_msg(outline, arg_found, ends_bkslash, ncode):
            arg_start_fmt=","
            dquote_fmt="\""
            endStr=");"
            max_idx = len(outline)
            if endStr in outline:
                    max_idx = outline.find(endStr)
            new_idx = 0
            comma_idx = 0
            arg_found = 0
            arg_first_idx = 0
            dq_idx = 0
            dq_count = 0
            if (arg_found == 1):
                return ("", outline, 1)
            dq_count = line.count(dquote_fmt)
                
#            if (arg_idx != -1):
#                print "comma found@ ", arg_idx, "@line ", linenum, " n-quotes= ", outline[:arg_idx].count(dquote_fmt), "bkslash=", ends_bkslash
            arg_idx = outline.find(arg_start_fmt)
            while (new_idx > 0) and (outline[:arg_idx].count(dquote_fmt) %2 != ends_bkslash):
#                print "comma at newidx=", new_idx, " argidx=" , arg_idx , " in ", outline
#                print "ends bkslash ", ends_bkslash , " n-outline= ", outline[:arg_idx]
                arg_idx += new_idx
                new_idx = outline[arg_idx+1:].find(arg_start_fmt)
            arg_first_idx = outline[:arg_idx].rfind(dquote_fmt)
            if (arg_first_idx < 0):
                     arg_first_idx = 0
#            print "arg-comma-found-at ", arg_idx , " -in- ", outline
            if (arg_idx >0):
                msg_str = outline[:arg_idx]
                msg_str = outline[:arg_first_idx]
                arg_str = outline[arg_first_idx+1:max_idx]
                arg_found = 1
#                print "arg found split1 " , msg_str, " -and-at-", str(arg_idx), " ===  ", arg_str
            else:
                msg_str = outline[:]
                arg_str = ""
            print arg_found, " EC_", ncode, " " , outline.lstrip() 
            print arg_idx, "split gives ", outline[:arg_idx].lstrip(), " &&& ", outline[arg_idx:max_idx]
            print arg_first_idx, "split gives ", outline[:arg_first_idx].lstrip(), " &&& ", outline[arg_first_idx:max_idx]
            return (msg_str, arg_str, arg_found)

def reformatSpec(aline, count, linenum):
    num_args = 0
    arg_spec_sym = "%"
    index = 0;
    line = aline;
    newstr = ""
#    print aline
    index = line.find(arg_spec_sym);
    if (index <0):
      newstr = line
      num_args = 0;
    else: 
      while (index > -1):
        if (index == -1):
          break;
        num_args += 1;
        spec_len = 0;
        fmt = line[index+1:index+2+spec_len]
#        print "index @ start =" ,index
#        print "fmt = " , fmt
        if (fmt is "l"):
          spec_len = 1;
          fmt = line[index+1:index+2+spec_len]
          if (fmt == "ll"):
            spec_len = 2;
            fmt = line[index+1:index+2+spec_len]
            if (fmt != "llu"):
                print "errrr format ", fmt
        else:
          if ((fmt is "d") or (fmt is "s") or (fmt is "x") or (fmt is "p") or (fmt == "u") or (fmt is "X")):
            spec_len = 0 
          else : 
            if (fmt is "0"): 
                spec_len = 3;
            else:
                spec_len = 3;
            fmt = line[index+1:index+2+spec_len]
        if (spec_len != 3):
            print "errrr matched", line, linenum, " && fmt= ", fmt
            newstr = line[:index+1] + str(count+num_args) + "%"+ line[index+2+spec_len:]
        else: 
            spec_len = 2;
            print "errrr unmatched", line, linenum
            newstr = line;
        line = newstr;
#        print "line @ exit =", line
        index = line.find(arg_spec_sym, index+4+spec_len);
    return (newstr, count+num_args) 

def reformat(line, numcode, linenum):
    newstr = line
    err_str="VCM_LOG_ERRO"
    new_log_pfx="LOGG_ERROR"
    arg_spec_sym = "%"
    index = line.find(err_str)
    logStr = line.replace(err_str, new_log_pfx);
    newLogStr = logStr[:index+NEW_LOG_LENGTH+1]
#    how new codes are assigned in storage api ?
#    newLogStr += "EC_CPE_" + str(numcode) +", "
    (newSpecStr, count) = reformatSpec(line[index+PATTERN_LENGTH+1:], 0, linenum);
#    print "reformatspec= ", newstr
#    print "line= ", newLogStr
    outline = newLogStr + newSpecStr 
    return (outline,count) 

def replace_imsi_str_arg(line):
    imsi_str="VCM_IMSI_STR"
    be_imsi_str="VCM_BE_IMSI_STR"
    new_fmt_imsi_str="\"%u %u %u %u %u %u %u %u %u %u %u %u %u %u %u\""
    new_fmt_imsi_str1="%u%u%u%u%u%u%u%u%u%u%u%u%u%u%u\""
    outline =""
    dq_str="\""
    dq_index = 0
    gen_imsi_str=""
    found = 0
    if be_imsi_str in line:
        found = 1
        gen_imsi_str = be_imsi_str
    if imsi_str in line:
        found = 1
        gen_imsi_str = imsi_str
    if (found == 0):
        return line
    dq_index = line.find(gen_imsi_str)
    dq_index = line[:dq_index].rfind(dq_str)
    outline = line.replace(gen_imsi_str, new_fmt_imsi_str)
    if (dq_index >0):
        pline = outline[:dq_index] + outline[dq_index:]
        pline = outline
    else: 
        pline = outline
    return pline

def replace_imsi_str(line):
    imsi_str="VCM_IMSI_STR"
    be_imsi_str="VCM_BE_IMSI_STR"
    new_fmt_imsi_str="\"%u %u %u %u %u %u %u %u %u %u %u %u %u %u %u\""
    new_fmt_imsi_str1="%u%u%u%u%u%u%u%u%u%u%u%u%u%u%u\""
    outline =""
    dq_str="\""
    dq_index = 0
    gen_imsi_str=""
    found = 0
    if be_imsi_str in line:
        found = 1
        gen_imsi_str = be_imsi_str
    if imsi_str in line:
        found = 1
        gen_imsi_str = imsi_str
    if (found == 0):
        return line
    dq_index = line.find(gen_imsi_str)
    dq_index = line[:dq_index].rfind(dq_str)
    outline = line.replace(gen_imsi_str, new_fmt_imsi_str)
    if (dq_index >0):
        pline = outline[:dq_index] + outline[dq_index:]
        pline = outline
    else: 
        pline = outline
#    print line , outline
#                    print_imsi_str(filename, linenum)
#1                    print filename.rstrip(), " PRINTS_IMSI_AT ", linenum, " ", outline, "  ", line
#    print " replace for ", line 
#    print " did ", outline , "with dqidx= ", str(dq_index)
#    print " replace returned ", pline 
    return pline

# assumes no arguments will have dbl quotes embedded
def split_line(outline, arg_found, str_mode, ncode):
            endStr=");"
            max_idx = len(outline)
            if endStr in outline:
                    max_idx = outline.find(endStr)

            dquote_fmt="\""
            found = 0
            mode = 0
            msg_str =""
            arg_str =""
            pfx_len = len(outline) - len(outline.lstrip(' '))
            pfx_str = outline[:pfx_len]
#            if (arg_found == 1):
#                return ("", outline, 1)

            last_dq_idx= outline.rfind(dquote_fmt)
            if (last_dq_idx == -1):
                if (str_mode):
                    msg_str = outline[:]
                    arg_str = ");\n"
                    found = 0
                    mode = 1
                else:
                    msg_str = ""
                    arg_str = outline
                    found = 1
                    mode = 0
#                    return ("", outline[:max_idx], 1, 0)
            else:
              if (outline[last_dq_idx -1] == "\\"):
                    msg_str = outline[:max_idx]
                    arg_str = ");\n"
                    found = 0
                    mode = 1
#                    return (outline[:max_idx], "", 0, 1)
              else:
                    msg_str = outline[:last_dq_idx+1]
                    arg_str = pfx_str + outline[last_dq_idx+1:]
                    found = 1
                    mode = 0
#                    return (outline[:last_dq_idx+1],outline[last_dq_idx:max_idx], 1, 0)
#            print  ncode, outline
#            print  ncode, " has msg= ", msg_str, "arg= ", arg_str, "found= ", found, "mode= ", mode, "dq= ", last_dq_idx
            return (msg_str, arg_str, found, mode)

def process(filename, errcode_jsonfilename, errcode_prefix, codenum, old_and_new):
#    destfile = open("../../"+filename.rstrip()+"1", 'w')
    destfile = open(filename.rstrip(), 'w')
#1    destfile = open("../../filename1", 'w')
    srcfile = open("../../"+filename.rstrip() , 'r')
#1    srcfile = open(filename.rstrip() , 'r')
    errcode_jsonfile = open(errcode_jsonfilename, 'a')
    errcode_hdrfile = open("defines.hpp", 'a')
    imsi_str="_IMSI_STR"
    aline = ""
    print filename 
    hdr_str="@date"
    hdr_str_found = 0
#    new_hdr_str="#include \"logs.h\" \n#include \"logg.hpp\" \n"
    new_hdr_str="\n#include \"logs.hpp\" \n"
    new_hdr_added = 0
    json_ncode_str="            \"code\"   : "
    json_mcode_str="            \"message\": "
    json_msg_indent_str="                        "
    json_ccode_str="            \"cause\"  : \" System Error \",\n"
    json_acode_str="            \"action\" : \"Contact Tech-Support\"\n"
    code_close_str="        }"
    code_cont_str =", {\n"
    comma_newline=",\n"
    err_str="VCM_LOG_ERRO"
    new_log_pfx="LOGG_ERROR"
    endStr=");"
    ends_bkslash = 0
    linenum=0
    numcode = codenum
    new_log_str =""
    str_mode = 0
    for line in srcfile:
        linenum += 1
        count = 0
        if (new_hdr_added == 0): 
            if (hdr_str_found == 0) and (hdr_str not in line):
                destfile.write(line)
                continue
            else:
                hdr_str_found = 1
            if (not line.isspace()):
                destfile.write(line)
                continue
            new_hdr_added = 1
            destfile.write(new_hdr_str)
        if err_str in line:
            if(numcode != codenum):
                errcode_jsonfile.write(code_cont_str)
            numcode += 1
            aline = replace_imsi_str(line)
            (outline, count) = reformat(aline, numcode, linenum)
            arg_pfx_len = outline.find(new_log_pfx)+len(new_log_pfx)+1
#            (msg_str, arg_str, arg_found) = fetch_msg(outline[arg_pfx_len:], 0, 0, numcode)
            (msg_str, arg_str, arg_found, str_mode) = split_line(outline[arg_pfx_len:], 0, 0, numcode)
            new_log_str += outline[:arg_pfx_len] + errcode_prefix + str(numcode)+ arg_str
            errcode_offset = line.find(err_str)
            errcode_offset = line[errcode_offset+1:].find("(") +1
            line_with_code = line[:errcode_offset+1] +  "\""+ errcode_prefix + str(numcode)+  ": \"" +line[errcode_offset+1:]
            if (old_and_new):
                destfile.write(line_with_code)
            errcode_jsonfile.write(json_ncode_str+ errcode_prefix + str(numcode)+": "+str(linenum)+
                                   comma_newline+ json_mcode_str + msg_str)
            errcode_hdrfile.write("#define " + errcode_prefix + str(numcode) + "  " + msg_str )
            while endStr not in line:
                line = srcfile.next()
                linenum += 1
                aline = replace_imsi_str(line)
#                print line, "\n", aline
                (outline, count) = reformatSpec(aline, count, linenum)
                (msg_str, arg_str, arg_found, str_mode) = split_line(outline, arg_found, str_mode, numcode)
                errcode_jsonfile.write(msg_str.lstrip())
                errcode_hdrfile.write(msg_str.lstrip())
                if (arg_str.strip() != ""):
                    new_log_str += arg_str
                if (old_and_new):
                    destfile.write(line)
#                print "new-log-str= ", new_log_str
#            destfile.write(new_log_str)
            errcode_hdrfile.write("\n")
            new_log_str=""
            errcode_jsonfile.write(comma_newline+ json_ccode_str + json_acode_str + code_close_str)
        else: 
            destfile.write(line)
    if (new_hdr_added == 0): 
        print filename.rstrip(), "file missing header -- errrr"
    errcode_jsonfile.close()
    srcfile.close()
    destfile.close()
    return numcode

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

def main(argv):
#    cmd="""find . -name "*.c" -o -name "*.cpp" > files-src.out"""
#    os.system(cmd)
    filelist=open("fsm_epc_attach_src.out", 'r')
    json_hdr = "{\n        \"logs\": [{\n"
    json_close_str="\n}\n"
    code_cont_str =", {\n"
    errcode_prefix="EC_CPE_FSM_EPC_ATTACH_"
    errcode_jsonfilename = "../../jsonfile1"
    errcode_jsonfile = open(errcode_jsonfilename, 'w')
    errcode_jsonfile.write(json_hdr)
    errcode_jsonfile.close()
    codenum = 1
    numcode = 1
    num_bkslash = 0
    old_and_new = 1
    for filename in filelist:
#        num_bkslash += bkslash_end(filename);
        if ((numcode != 1) and (numcode != codenum)):
            errcode_jsonfile = open(errcode_jsonfilename, 'a')
            errcode_jsonfile.write(code_cont_str)
            errcode_jsonfile.close()
            codenum = numcode
        numcode = process(filename, errcode_jsonfilename, errcode_prefix, codenum, old_and_new)
    print " num_bkslash = ", num_bkslash
    errcode_jsonfile = open(errcode_jsonfilename, 'a')
    errcode_jsonfile.write(json_close_str)
    errcode_jsonfile.close()

if __name__ == "__main__":
    main(sys.argv)
