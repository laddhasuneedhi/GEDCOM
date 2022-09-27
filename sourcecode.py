#I pledge my honor that I have abided by the Stevens Honors System.
# https://github.com/laddhasuneedhi/Project02.git
#Hao Dian Li, Suneedhi Laddha, Ali El Sayed,Gigi Luna

from platform import java_ver
import sys
import os #Hack to make colors work in Windows cmd 1/2
os.system('color') #Hack to make colors work in Windows cmd 2/2
from prettytable import PrettyTable
from datetime import date

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
# print ("Analyzing: " + str(sys.argv))

x = PrettyTable()
y = PrettyTable()
x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
y.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

# define variables for table x 
tblx_id = "N/A"; tblx_name = "N/A"; tblx_gend = "N/A"; tblx_birt = "N/A"; tblx_age = "N/A"; tblx_aliv = "N/A"; tblx_deat = "N/A"; tblx_chil = "N/A"; tblx_spou = "N/A"
tbly_id = "N/A"; tbly_marr = "N/A"; tbly_divo = "N/A"; tbly_husi = "N/A"; tbly_husn = "N/A"; tbly_wifi = "N/A"; tbly_wifn = "N/A"; tbly_chil = "N/A"
birfday = 0; deafday = 0; todays_date = date.today(); tblx_sarr = []; tblx_carr = []; marfday = 0; divfday = 0; tbly_carr = []
name_list = []; id_list = []

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
        # print("--> " + line)

    #output
        i = a+1
        linelen = (len(ogline))
        while ogline[i] != " " and ogline[i] != '\n': #identify last index of second token
            if a+1+i > linelen:
                # if line[a+1:i+1] in validtags: #second token is a valid tag
                #     if (level == "1") and (line[a+1:i+1] in singletag):
                #         if line[a+1:i+1] == "NAME": print("<-- " + level + "|" + line[a+1:i+1] + "|Y|")
                #     else:
                #         #raise ValueError('Invalid level with the tag: <' + line[a+1:i+1] + '>')
                #         print("Invalid level: <" + level + "> with the tag: <" + line[a+1:i+1] + ">")
                # else:
                #     print("<-- " + level + "|" + line[a+1:i+1] + "|N|")
                quit()
            else:
                i+=1
        tag = line[a+1:i] #second token

        if tag in validtags: #second token is a valid tag

            # if (line[0] == "0") and (tag in tag0):
            #     print("<-- " + level + "|" + tag + "|Y|" + line[i+1:])
            # elif (line[0] == "1") and (tag in tag1):
            if (line[0] == "1") and (tag in tag1):

                # print("<-- " + level + "|" + tag + "|Y|" + line[i+1:])
                if (tag == "NAME"): 
                    tblx_name = line[i+1:]
                    name_list.append(tblx_name)
                    id_list.append(tblx_id)

                if (tag == "SEX"): tblx_gend = line[i+1:]
                if (tag == "BIRT"): birfday = 1
                if (tag == "DEAT"): deafday = 1
                if (tag == "FAMC"): tblx_carr.append(line[i+1:]); tblx_chil = tblx_carr
                if (tag == "FAMS"): tblx_sarr.append(line[i+1:]); tblx_spou = tblx_sarr

                if (tag == "MARR"): marfday = 1
                if (tag == "DIV"): divfday = 1
                if (tag == "CHIL"): tbly_carr.append(line[i+1:]); tbly_chil = tbly_carr
                if (tag == "HUSB"): 
                    m = line[i+1:].rstrip()
                    tbly_husi = m
                    tbly_husn = name_list[id_list.index(m)]               

                if (tag == "WIFE"): 
                    m = line[i+1:].rstrip()
                    tbly_wifi = m
                    tbly_wifn = name_list[id_list.index(m)]

            elif (line[0] == "2") and (tag in tag2):
                # print("<-- " + level + "|" + tag + "|Y|" + line[i+1:])
                if (tag == "DATE"): 
                    if (birfday == 1): tblx_birt = line[i+1:]; birfday = 0
                    if (deafday == 1): tblx_deat = line[i+1:]; deafday = 0; tblx_aliv = False

                    if (marfday == 1): tbly_marr = line[i+1:]; marfday = 0
                    if (divfday == 1): tbly_divo = line[i+1:]; divfday = 0
            # else:
                #raise ValueError('Invalid level with the tag: <' + tag + '>')
                # print("Invalid level: <" + level + "> with the tag: <" + tag + ">.")

        else: #second token is not a valid tag, we look at third token :)
            
            tag = line[i+1:]

            if tag in validtags:
                if tag in extag: #INDI, FAM only
                    if (line[0] == "0"):
                        # print("<-- " + line[0] + "|" + tag + "|Y|" + line[2:i+1])
                        if (tag == "INDI"):
                            # check if we've been here before and write-out then clear previous table data if we have
                            if (tblx_id != "N/A"):
                                # print (red + "Next Customer!" + white)

                                birth_split = tblx_birt.split(" ")
                                death_split = tblx_deat.split(" ")
                                if tblx_aliv == True:
                                    tblx_age = todays_date.year - int(birth_split[2])
                                elif tblx_aliv == False:
                                    tblx_age = int(death_split[2]) - int(birth_split[2])
                                    
                                x.add_row([tblx_id, tblx_name, tblx_gend, tblx_birt, tblx_age, tblx_aliv, tblx_deat, tblx_chil, tblx_spou])
                                tblx_id = "N/A"; tblx_name = "N/A"; tblx_gend = "N/A"; tblx_birt = "N/A"; tblx_age = "N/A"; tblx_aliv = "N/A"; tblx_deat = "N/A"; tblx_chil = "N/A"; tblx_spou = "N/A"; tblx_carr = []; tblx_sarr = []
                                tblx_id = line[2:i+1].rstrip()
                                tblx_aliv = True
                            elif (tblx_id == "N/A"):
                                tblx_id = line[2:i+1].rstrip()
                                tblx_aliv = True
                        if (tag == "FAM"):
                            # reset table y from 0 terminater
                            if (tbly_id != "N/A"):
                                y.add_row([tbly_id, tbly_marr, tbly_divo, tbly_husi, tbly_husn, tbly_wifi, tbly_wifn, tbly_chil])
                                tbly_id = "N/A"; tbly_marr = "N/A"; tbly_divo = "N/A"; tbly_husi = "N/A"; tbly_husn = "N/A"; tbly_wifi = "N/A"; tbly_wifn = "N/A"; tbly_chil = "N/A"; tbly_carr = []
                                tbly_id = line[2:i+1]
                            elif (tbly_id == "N/A"):
                                tbly_id = line[2:i+1]
                    # else:
                        #raise ValueError('Invalid level with the tag: <' + tag + '>')
                        # print("Invalid level: <" + level + "> with the tag: <" + tag + ">.")
                # else:
                    #raise ValueError('Only tags valid for this format: ' + extag)
                    # print("Only tags valid for this format: " + extag)
            # else: #no valid tag provided
                # print("<-- " + level + "|" + line[a+1:i] + "|" + red + "N" + white + "|" + tag)

    else:
        if ogline[0] == '\n':
            line = line.strip('\n')
        # else:
        #     line = line.strip('\n')
        #     print("--> " + line)
        #     #raise ValueError('Invalid level: <' + level + '>')
        #     print("Invalid level: <" + level + ">")
# """

#this is INDI table
# capture the last table entry since there are no more terminaters (0)
birth_split = tblx_birt.split(" ")
death_split = tblx_deat.split(" ")
if tblx_aliv == True:
    tblx_age = todays_date.year - int(birth_split[2])
elif tblx_aliv == False:
    tblx_age = int(death_split[2]) - int(birth_split[2])
    
x.add_row([tblx_id, tblx_name, tblx_gend, tblx_birt, tblx_age, tblx_aliv, tblx_deat, tblx_chil, tblx_spou])

y.add_row([tbly_id, tbly_marr, tbly_divo, tbly_husi, tbly_husn, tbly_wifi, tbly_wifn, tbly_chil])

print("Individuals")
print(x.get_string(sortby = "ID"))
print("Families")
print(y.get_string(sortby = "ID"))

f.close()