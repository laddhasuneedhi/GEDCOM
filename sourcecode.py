#I pledge my honor that I have abided by the Stevens Honors System.
#Hao Dian Li

import sys
import os #Hack to make colors work in Windows cmd 1/2
os.system('color') #Hack to make colors work in Windows cmd 2/2
from prettytable import PrettyTable

validtags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
tag0 = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
tag1 = ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"]
tag2 = ["DATE"]
extag = ["INDI", "FAM"]
singletag = ["MARR", "DIV"]
validlevels = ["0", "1", "2"]

if len(sys.argv) == 1:
	print ("\nPlease provide input filename as the first argument and try again.\n")
	quit()
	
arg_0 = sys.argv[0]
arg_1 = sys.argv[1]

# Color definitions
dark_red = "\033[0;31m"
red = "\033[0;91m"
white = "\033[0;37m"

f = open(arg_1, 'r')
print ("Analyzing: " + str(sys.argv))

x = PrettyTable()
y = PrettyTable()
x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
y.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

# define variables for table x 
tbl_id = None; tbl_name = None; tbl_gend = None; tbl_birt = None; tbl_age = None; tbl_aliv = None; tbl_deat = None; tbl_chil = None; tbl_spou = None

# define variables for table y

# """
for line in f:

    ogline = line

    a = 0
    while ogline[a] != " " and ogline[a] != '\n': #identify last index of first token
        a+=1
    level = line[0:a] #first token

    #input
    if level in validlevels:
        line = line.strip('\n')
        print("--> " + line)

    #output
        i = a+1
        linelen = (len(ogline))
        while ogline[i] != " " and ogline[i] != '\n': #identify last index of second token
            if a+1+i > linelen:
                if line[a+1:i+1] in validtags: #second token is a valid tag
                    if (level == "1") and (line[a+1:i+1] in singletag):
                        if line[a+1:i+1] == "NAME": print("<-- " + level + "|" + line[a+1:i+1] + "|Y|")
                    else:
                        #raise ValueError('Invalid level with the tag: <' + line[a+1:i+1] + '>')
                        print("Invalid level: <" + level + "> with the tag: <" + line[a+1:i+1] + ">")
                else:
                    print("<-- " + level + "|" + line[a+1:i+1] + "|N|")
                quit()
            else:
                i+=1
        tag = line[a+1:i] #second token

        if tag in validtags: #second token is a valid tag

            if (line[0] == "0") and (tag in tag0):
                print("<-- " + level + "|" + tag + "|Y|" + line[i+1:])
            elif (line[0] == "1") and (tag in tag1):
                print("<-- " + level + "|" + tag + "|Y|" + line[i+1:])
                if (tag == "NAME"): tbl_name = line[i+1:]
                if (tag == "SEX"): tbl_gend = line[i+1:]
            elif (line[0] == "2") and (tag in tag2):
                print("<-- " + level + "|" + tag + "|Y|" + line[i+1:])
                #if (tag == "DEAT"): tbl_alive = "he need some milk"
            else:
                #raise ValueError('Invalid level with the tag: <' + tag + '>')
                print("Invalid level: <" + level + "> with the tag: <" + tag + ">.")

        else: #second token is not a valid tag, we look at third token
            
            tag = line[i+1:]

            if tag in validtags:
                if tag in extag: #INDI, FAM only
                    if (line[0] == "0"):
                        print("<-- " + line[0] + "|" + tag + "|Y|" + line[2:i+1])
                        if (tag == "INDI"):
                            # check if we've been here before and write-out then clear previous table data if we have
                            if (tbl_id != None):
                                print (red + "Next Customer!" + white)
                                x.add_row([tbl_id, tbl_name, tbl_gend, tbl_birt, tbl_age, tbl_aliv, tbl_deat, tbl_chil, tbl_spou])
                                tbl_id = None; tbl_name = None; tbl_gend = None; tbl_birt = None; tbl_age = None; tbl_aliv = None; tbl_deat = None; tbl_chil = None; tbl_spou = None
                                tbl_id = line[2:i+1]
                            elif (tbl_id == None):
                                tbl_id = line[2:i+1]
                        if (line[2:i+1] == "FAM"):
                            # reset table y from 0 terminater
                            tbl_id = None;
                    else:
                        #raise ValueError('Invalid level with the tag: <' + tag + '>')
                        print("Invalid level: <" + level + "> with the tag: <" + tag + ">.")
                else:
                    #raise ValueError('Only tags valid for this format: ' + extag)
                    print("Only tags valid for this format: " + extag)
            else: #no valid tag provided
                print("<-- " + level + "|" + line[a+1:i] + "|" + red + "N" + white + "|" + tag)

    else:
        if ogline[0] == '\n':
            line = line.strip('\n')
        else:
            line = line.strip('\n')
            print("--> " + line)
            #raise ValueError('Invalid level: <' + level + '>')
            print("Invalid level: <" + level + ">")
# """

# capture the last table entry since there are no more terminaters (0)
x.add_row([tbl_id, tbl_name, tbl_gend, tbl_birt, tbl_age, tbl_aliv, tbl_deat, tbl_chil, tbl_spou])
# y.add_row([bla,bla])
print(x)


f.close()