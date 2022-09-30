# I pledge my honor that I have abided by the Stevens Honors System.
# https://github.com/laddhasuneedhi/Project02.git
# Hao Dian Li, Suneedhi Laddha, Ali El Sayed, Gigi Luna

import sys
from prettytable import PrettyTable
from datetime import date, datetime
import calendar
from datetime import datetime

validtags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
tag0 = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
tag1 = ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"]
tag2 = ["DATE"]
extag = ["INDI", "FAM"]
singletag = ["BIRT", "MARR", "DIV"]
validlevels = ["0", "1", "2"]

if len(sys.argv) == 1:
	print ("\nPlease provide input filename as the first argument and try again.\n")
	quit()
	
arg_0 = sys.argv[0]
arg_1 = sys.argv[1]

f = open(arg_1, 'r')

x = PrettyTable()
y = PrettyTable()
x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
y.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

birfday = 0; deafday = 0; todays_date = date.today()
name_list = []
id_list = []

tblx_id = "N/A"; tblx_name = "N/A"; tblx_gend = "N/A"; tblx_birt = "N/A"; tblx_age = "N/A"; tblx_aliv = "N/A"; tblx_deat = "N/A"; tblx_chil = "N/A"; tblx_spou = "N/A"
tbly_id = "N/A"; tbly_marr = "N/A"; tbly_divo = "N/A"; tbly_husi = "N/A"; tbly_husn = "N/A"; tbly_wifi = "N/A"; tbly_wifn = "N/A"; tbly_chil = "N/A"
birfday = 0; deafday = 0; todays_date = date.today(); tblx_sarr = []; tblx_carr = []; marfday = 0; divfday = 0; tbly_carr = []
name_list = []; id_list = []

def _matchId(id):
    
    gotmatch = 0
    fcopy = open(arg_1, 'r')

    for line in fcopy:

        matchToken = line.split() #list of the line
        matchStrList = matchToken[2:]
        matchFullStr = ' '.join(str(i) for i in matchStrList)
        if line == "\n": continue #ignore the empty lines
        if (int(matchToken[0]) == 0) and (gotmatch == 1) and (matchToken[2] == "INDI" or "FAM"): return "N/A"
        if (int(matchToken[0]) == 0) and (matchToken[1] == id): gotmatch = 1
        if (int(matchToken[0]) == 1) and (matchToken[1] == "NAME") and (gotmatch == 1): gotmatch = 0; matchFullStr = ' '.join(str(i) for i in matchStrList); return matchFullStr; print (matchFullStr)
    
    fcopy.close()

def age(given_date, birthdate):

    age = given_date.year - birthdate.year - ((given_date.month, given_date.day) < (birthdate.month, birthdate.day))
    return age

# """
for line in f:

    token = line.split() #list of the line
    numtok = len(token)

    if line == "\n": continue #ignore the empty lines

    tok0 = int(token[0]) #first token: level 012

    if (tok0 < 0) or (tok0 > 2): print("Invalid level.") #checks for invalid level

    tok1 = token[1] #second token: tags

    if tok1 in validtags: #check if second token is a valid tag
        # if numtok < 3: #only a tag is present, no string        ex: 1 BIRT/MARR/DIV
        #     print("todo: " + tok1)

        # #level 0 tags
        # if (tok0 == 0) and (tok1 in tag0): #INDI and FAM does not pass this if statement
        #     print("Debug: Level " + str(tok0) + ", but it's not important.")

        #level 1 tags
        strList = token[2:]
        fullStr = ' '.join(str(i) for i in strList)

        if (tok0 == 1) and (tok1 in tag1):

            if tok1 == "NAME": tblx_name = fullStr
            if tok1 == "DIV": divfday = 1
            if tok1 == "BIRT": birfday = 1
            if tok1 == "DEAT": deafday = 1
            if tok1 == "MARR": marfday = 1
            if tok1 == "SEX": tblx_gend = fullStr
            if tok1 == "FAMC": tblx_carr.append(fullStr); tblx_chil = tblx_carr
            if tok1 == "FAMS": tblx_sarr.append(fullStr); tblx_spou = tblx_sarr
            if tok1 == "CHIL": tbly_carr.append(fullStr); tbly_chil = tbly_carr
            if tok1 == "WIFE":
                tbly_wifi = fullStr
                matchName = _matchId(tbly_wifi)
                tbly_wifn = matchName
            if tok1 == "HUSB":
                tbly_husi = fullStr
                matchName = _matchId(tbly_husi)
                tbly_husn = matchName

        #level 2 tags
        elif (tok0 == 2) and (tok1 in tag2):
            if tok1 == "DATE":
                if birfday == 1: tblx_birt = fullStr; birfday = 0
                if deafday == 1: tblx_deat = fullStr; deafday = 0; tblx_aliv = False
                if marfday == 1: tbly_marr = fullStr; marfday = 0
                if divfday == 1: tbly_divo = fullStr; divfday = 0
    
    else: #check if third token is a valid tag   ex: INDI or FAM

        tok2 = token[2]

        if tok2 in extag:
            if tok2 == "INDI":
                if tblx_id != "N/A":
                    
                    # calculate accurate ages
                    today = date.today()
                    birth_split = tblx_birt.split()
                    death_split = tblx_deat.split()
                    # convert month name to number  ex: May -> 5
                    abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
                    bmn_to_num = abbr_to_num[birth_split[1]]

                    if tblx_aliv == True: tblx_age = age(today, date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))
                    elif tblx_aliv == False:
                        dmn_to_num = abbr_to_num[death_split[1]]
                        tblx_age = age(date(int(death_split[2]), dmn_to_num, int(death_split[0])), date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))

                    x.add_row([tblx_id, tblx_name, tblx_gend, tblx_birt, tblx_age, tblx_aliv, tblx_deat, tblx_chil, tblx_spou])
                    tblx_id = "N/A"; tblx_name = "N/A"; tblx_gend = "N/A"; tblx_birt = "N/A"; tblx_age = "N/A"; tblx_aliv = "N/A"; tblx_deat = "N/A"; tblx_chil = "N/A"; tblx_spou = "N/A"; tblx_carr = []; tblx_sarr = []
                    tblx_id = tok1
                    tblx_aliv = True

                elif tblx_id == "N/A":

                    tblx_id = tok1
                    tblx_aliv = True

            if tok2 == "FAM":
                if tbly_id != "N/A":
                    y.add_row([tbly_id, tbly_marr, tbly_divo, tbly_husi, tbly_husn, tbly_wifi, tbly_wifn, tbly_chil])
                    tbly_id = "N/A"; tbly_marr = "N/A"; tbly_divo = "N/A"; tbly_husi = "N/A"; tbly_husn = "N/A"; tbly_wifi = "N/A"; tbly_wifn = "N/A"; tbly_chil = "N/A"; tbly_carr = []
                    tbly_id = tok1

                elif tbly_id == "N/A":
                    tbly_id = tok1

        # else: 
        #     print("Invalid tag as 3rd token")

today = date.today()
birth_split = tblx_birt.split()
death_split = tblx_deat.split()
abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
bmn_to_num = abbr_to_num[birth_split[1]]

if tblx_aliv == True: tblx_age = age(today, date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))
elif tblx_aliv == False:
    dmn_to_num = abbr_to_num[death_split[1]]
    tblx_age = age(date(int(death_split[2]), dmn_to_num, int(death_split[0])), date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))

x.add_row([tblx_id, tblx_name, tblx_gend, tblx_birt, tblx_age, tblx_aliv, tblx_deat, tblx_chil, tblx_spou])
y.add_row([tbly_id, tbly_marr, tbly_divo, tbly_husi, tbly_husn, tbly_wifi, tbly_wifn, tbly_chil])

# """
print("Individuals")
print(x.get_string(sortby = "ID"))
print("Families")
print(y.get_string(sortby = "ID"))

f.close()