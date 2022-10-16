# I pledge my honor that I have abided by the Stevens Honors System.
# https://github.com/laddhasuneedhi/Project02.git
# Hao Dian Li, Suneedhi Laddha, Ali El Sayed, Gigi Luna

import sys
from prettytable import PrettyTable
from datetime import date, timedelta

validtags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM",
             "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
tag0 = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
tag1 = ["NAME", "SEX", "BIRT", "DEAT", "FAMC",
        "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"]
tag2 = ["DATE"]
extag = ["INDI", "FAM"]
singletag = ["BIRT", "MARR", "DIV"]
validlevels = ["0", "1", "2"]

# if len(sys.argv) == 1:
# 	print ("\nPlease provide input filename as the first argument and try again.\n")
# 	quit()

# arg_0 = sys.argv[0]
# arg_1 = sys.argv[1]

arg_0 = sys.argv[0]
arg_1 = "famtreeus03us04.ged"

f = open(arg_1, 'r')

x = PrettyTable()
y = PrettyTable()
x.field_names = ["ID", "Name", "Gender", "Birthday",
                 "Age", "Alive", "Death", "Child", "Spouse"]
y.field_names = ["ID", "Married", "Divorced", "Husband ID",
                 "Husband Name", "Wife ID", "Wife Name", "Children"]
kids_born = {}
birfday = 0
deafday = 0
todays_date = date.today()
name_list = []
id_list = []

tblx_id = "N/A"
tblx_name = "N/A"
tblx_gend = "N/A"
tblx_birt = "N/A"
tblx_age = "N/A"
tblx_aliv = "N/A"
tblx_deat = "N/A"
tblx_chil = "N/A"
tblx_spou = "N/A"
tbly_id = "N/A"
tbly_marr = "N/A"
tbly_divo = "N/A"
tbly_husi = "N/A"
tbly_husn = "N/A"
tbly_wifi = "N/A"
tbly_wifn = "N/A"
tbly_chil = "N/A"
birfday = 0
deafday = 0
todays_date = date.today()
tblx_sarr = []
tblx_carr = []
marfday = 0
divfday = 0
tbly_carr = []
tbly_sarr = []
tempbday = "N/A"
tempdday = "N/A"
tempmday = "N/A"
tempvday = "N/A"
us05tempmday = "N/A"
us05tempdday = "N/A"
us10tempbday = "N/A"
us10tempmday = "N/A"
deadList = []
us03List = []
us04List = []
us05List = []
us06List = []
us07ListA = []
us07ListB = []
us10List = []
us36List = []
us27List = []
us28List = []
us42List = []


abbr_to_num = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5,
               'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

abbr_to_strMonth = {'1' : 'JAN', '2' : 'FEB', '3' : 'MAR', '4' : 'APR', '5':'MAY', '6':'JUN'
,'7' : 'JUL','8' : 'AUG','9' : 'SEP','10' : 'OCT','11' : 'NOV','12' : 'DEC'}

# helper functions

def _matchId(id):

    gotmatch = 0
    fcopy = open(arg_1, 'r')

    for line in fcopy:

        matchToken = line.split()  # list of the line
        matchStrList = matchToken[2:]
        matchFullStr = ' '.join(str(i) for i in matchStrList)
        if line == "\n":
            continue  # ignore the empty lines
        if (int(matchToken[0]) == 0) and (gotmatch == 1) and (matchToken[2] == "INDI" or "FAM"):
            return "N/A"
        if (int(matchToken[0]) == 0) and (matchToken[1] == id):
            gotmatch = 1
        if (int(matchToken[0]) == 1) and (matchToken[1] == "NAME") and (gotmatch == 1):
            gotmatch = 0
            matchFullStr = ' '.join(str(i) for i in matchStrList)
            return matchFullStr

    fcopy.close()


def _age(given_date, birthdate):

    age = given_date.year - birthdate.year - \
        ((given_date.month, given_date.day) < (birthdate.month, birthdate.day))
    return age

def _us09(husid, wifid, chilist):
    dad_age = kids_born[husid]
    mom_age = kids_born[wifid]
    dad_age = int((dad_age.split())[2])
    mom_age = int((mom_age.split())[2])
    for x in chilist:
        kid_age = kids_born[x]
        kid_age = int((kid_age.split())[2])
        if (mom_age - kid_age) > 0 or (dad_age - kid_age) > 0:
            return False
    return True

def _us03(bdate, ddate, id):

    # converts month name to a number
    bmn_to_num = abbr_to_num[bdate[1]]
    dmn_to_num = abbr_to_num[ddate[1]]
    # yyyy-mm-dd format
    birth_date = date(int(bdate[2]), bmn_to_num, int(bdate[0]))
    death_date = date(int(ddate[2]), dmn_to_num, int(ddate[0]))
    # find age difference
    age_diff = _age(death_date, birth_date)

    if age_diff < 0:

        # list of INDI who have negative ages
        s = [id, str(birth_date), str(death_date)]
        us03List.append(list(s))
        return us03List


def _us03print(list):

    for x in list:
        print("ERROR: INDIVIDUAL: US03: " +
              x[0] + ": Died " + x[2] + " before born " + x[1])


def _us04(mdate, vdate, id):
    
    marr_date = -1
    divo_date = -1
    year_status = False

    # converts month name to a number
    mmn_to_num = abbr_to_num[mdate[1]]
    vmn_to_num = abbr_to_num[vdate[1]]
    # yyyy-mm-dd format
    if _us42(int(mdate[2]), mmn_to_num, int(mdate[0])):
        marr_date = date(int(mdate[2]), mmn_to_num, int(mdate[0]))
    else:
        s = [id, 2, int(mdate[2]), mmn_to_num, int(mdate[0])]
        if s in us42List:
            pass
        else:
            us42List.append(s)
    
    if _us42(int(vdate[2]), vmn_to_num, int(vdate[0])):
        divo_date = date(int(vdate[2]), vmn_to_num, int(vdate[0]))
    else:
        s = [id, 3, int(vdate[2]), vmn_to_num, int(vdate[0])]
        if s in us42List:
            pass
        else:
            us42List.append(s)
    # find age difference
    if (marr_date != -1) and (divo_date != -1):
        year_diff = _age(divo_date, marr_date)
        year_status = True

    if (year_status == True) and (year_diff < 0):

        # list of INDI who have negative ages
        s = [id, str(marr_date), str(divo_date)]
        us04List.append(list(s))
        return us04List


def _us04print(list):

    for x in list:
        print("ERROR: FAMILY: US04: " +
              x[0] + ": Divorced " + x[2] + " before married " + x[1])

def _us06(sarr, div, wifi, husi, fid):
    # print(sarr)

    age_diff = -1
    gotmatch = 0
    gotdeath = 0
    death = "N/A"
    lookupID = "N/A"
    div = div.split()
    fcopy = open(arg_1, 'r')

    for line in fcopy:

        matchToken = line.split()  # list of the line

        if line == "\n":
            continue  # ignore the empty lines

        if (int(matchToken[0]) == 0) and (matchToken[1] != "NOTE") and gotmatch == 1:
            gotmatch = 0
            gotdeath = 0
        if (int(matchToken[0]) == 0) and ((matchToken[1] == sarr[0]) or (matchToken[1] == sarr[1])):
            gotmatch = 1
            lookupID = matchToken[1]
        if (int(matchToken[0]) == 1) and (matchToken[1] == "DEAT") and (gotmatch == 1):
            gotdeath = 1
        if (int(matchToken[0]) == 2) and (matchToken[1] == "DATE") and (gotdeath == 1):
            death = matchToken[2:]
            month_death = abbr_to_num[death[1]]
            month_div = abbr_to_num[divo_split[1]]
            if _us42(int(divo_split[2]), month_div, int(divo_split[0])):
                if _us42(int(death[2]), month_death, int(death[0])):
                    age_diff = _age(date(int(divo_split[2]), month_div, int(divo_split[0])), date(int(death[2]), month_death, int(death[0])))
                else: 
                    s = [fid, 2, int(death[2]), month_death, int(death[0])]
                    if s in us42List:
                        pass
                    else: us42List.append(s)
            else:
                s = [fid, 3, int(divo_split[2]), month_div, int(divo_split[0])]
                if s in us42List:
                    pass
                else:
                    us42List.append(s)
            gotmatch = 0
            gotdeath = 0
            if age_diff >= 0:
                odeath = date(int(death[2]), month_death, int(death[0]))
                div_formatted = date(int(div[2]), month_div, int(div[0]))
                if lookupID == wifi:
                    s_type = "wife"
                if lookupID == husi:
                    s_type = "husband"
                us06List.append(
                    [lookupID, str(odeath), str(div_formatted), s_type, fid])
                # return us06List
            # else: gotmatch = 0; gotdeath = 0

    fcopy.close()
    return us06List


def _us06print(list):

    for x in list:
        print("ERROR: FAMILY: US06:", x[4] + ": Divorced", x[2],
              "after", x[3] + "'s (" + x[0] + ") death on", x[1])

def _us07a(bdate, ddate, id):

    # converts month name to a number
    bmn_to_num = abbr_to_num[bdate[1]]
    dmn_to_num = abbr_to_num[ddate[1]]
    # yyyy-mm-dd format
    birth_date = date(int(bdate[2]), bmn_to_num, int(bdate[0]))
    death_date = date(int(ddate[2]), dmn_to_num, int(ddate[0]))
    # find age difference
    age_diff = _age(death_date, birth_date)

    if age_diff >= 150:

        s = [id, str(birth_date), str(death_date)]
        us07ListA.append(list(s))
        return us07ListA


def _us07Aprint(list):

    for x in list:
        print("ERROR: INDIVIDUAL: US07: " +
              x[0] + " Death should less than 150 years")


def _us07b(bdate, tdate, id):

    bmn_to_num = abbr_to_num[bdate[1]]
    tmn_to_num = abbr_to_num[abbr_to_strMonth[tdate[1]]]
    # yyyy-mm-dd format
    birth_date = date(int(bdate[2]), bmn_to_num, int(bdate[0]))
    todaydate = date(int(tdate[0]), tmn_to_num, int(tdate[2]))

    diff = _age(todaydate, birth_date)

    if diff >= 150:

        s = [id, str(birth_date)]
        us07ListB.append(list(s))
        return us07ListB



def _us07bprint(list):

    for x in list:
        print("ERROR: INDIVIDUAL: US07: " +
              x[0] + " Current Date should be less than 150 years after birth")

#this was implemented by Suneedhi Laddha and Hao Dian Li
def _us15(fam_id, list_of_kids):
    if len(list_of_kids) > 15:
        print("for fam:", fam_id, "children is greater than 15")
        return False
    else:
        return True

def _corpseBride(sarr, marr, wifi, husi, fid):
    # print(sarr)

    gotmatch = 0
    gotdeath = 0
    death = "N/A"
    lookupID = "N/A"
    marr = marr.split()
    age_diff = -1
    fcopy = open(arg_1, 'r')

    for line in fcopy:

        matchToken = line.split()  # list of the line

        if line == "\n":
            continue  # ignore the empty lines

        if (int(matchToken[0]) == 0) and (matchToken[1] != "NOTE") and gotmatch == 1:
            gotmatch = 0
            gotdeath = 0
        if (int(matchToken[0]) == 0) and ((matchToken[1] == sarr[0]) or (matchToken[1] == sarr[1])):
            gotmatch = 1
            lookupID = matchToken[1]
        if (int(matchToken[0]) == 1) and (matchToken[1] == "DEAT") and (gotmatch == 1):
            gotdeath = 1
        if (int(matchToken[0]) == 2) and (matchToken[1] == "DATE") and (gotdeath == 1):
            death = matchToken[2:]
            month_death = abbr_to_num[death[1]]
            month_marr = abbr_to_num[marr_split[1]]
            if _us42(int(marr_split[2]), month_marr, int(marr_split[0])):
                if _us42(int(death[2]), month_death, int(death[0])):
                    age_diff = _age(date(int(marr_split[2]), month_marr, int(marr_split[0])), date(int(death[2]), month_death, int(death[0])))
                else:
                    s = [lookupID, 1, int(death[2]), month_death, int(death[0])]
                    if s in us42List:
                        pass
                    else:
                        us42List.append(s)
            else:
                s = [lookupID, 2, int(marr_split[2]), month_marr, int(marr_split[0])]
                if s in us42List:
                    pass
                else:
                    us42List.append(s)
            gotmatch = 0
            gotdeath = 0
            if age_diff >= 0:
                if _us42(int(death[2]), month_death, int(death[0])):
                    odeath = date(int(death[2]), month_death, int(death[0]))
                else:
                    s = [lookupID, 1, int(death[2]), month_death, int(death[0])]
                    if s in us42List:
                        pass
                    else:
                        us42List.append(s)
                # odeath = date(int(death[2]), month_death, int(death[0]))
                marr_formatted = date(int(marr[2]), month_marr, int(marr[0]))
                if lookupID == wifi:
                    s_type = "wife"
                if lookupID == husi:
                    s_type = "husband"
                us05List.append(
                    [lookupID, str(odeath), str(marr_formatted), s_type, fid])
                # return us05List
            # else: gotmatch = 0; gotdeath = 0

    fcopy.close()
    return us05List


def _us05print(list):

    for x in list:
        print("ERROR: FAMILY: US05:", x[4] + ": Married", x[2],
              "after", x[3] + "'s (" + x[0] + ") death on", x[1])


def _us10(sarr, marr, wifi, husi, fid):
    # print(sarr)

    age_diff = -1
    gotmatch = 0
    gotbirth = 0
    birth = "N/A"
    lookupID = "N/A"
    marr = marr.split()
    fcopy = open(arg_1, 'r')

    for line in fcopy:

        matchToken = line.split()  # list of the line

        if line == "\n":
            continue  # ignore the empty lines

        if (int(matchToken[0]) == 0) and (matchToken[1] != "NOTE") and gotmatch == 1:
            gotmatch = 0
            gotbirth = 0
        if (int(matchToken[0]) == 0) and ((matchToken[1] == sarr[0]) or (matchToken[1] == sarr[1])):
            gotmatch = 1
            lookupID = matchToken[1]
        if (int(matchToken[0]) == 1) and (matchToken[1] == "BIRT") and (gotmatch == 1):
            gotbirth = 1
        if (int(matchToken[0]) == 2) and (matchToken[1] == "DATE") and (gotbirth == 1):
            birth = matchToken[2:]
            month_birth = abbr_to_num[birth[1]]
            month_marr = abbr_to_num[marr_split[1]]
            if _us42(int(marr_split[2]), month_marr, int(marr_split[0])):
                if _us42(int(birth[2]), month_birth, int(birth[0])):
                    age_diff = _age(date(int(marr_split[2]), month_marr, int(marr_split[0])), date(int(birth[2]), month_birth, int(birth[0])))
                else:
                    s = [lookupID, 0, int(birth[2]), month_birth, int(birth[0])]
                    if s in us42List:
                        pass
                    else:
                        us42List.append(s)
            else:
                s = [lookupID, 2, int(marr_split[2]), month_marr, int(marr_split[0])]
                if s in us42List:
                    pass
                else:
                    us42List.append(s)
            # age_diff = _age(date(int(marr_split[2]), month_marr, int(marr_split[0])), date(int(birth[2]), month_birth, int(birth[0])))
            gotmatch = 0
            gotbirth = 0
            if (age_diff != -1) and (age_diff < 14):
                obirth = date(int(birth[2]), month_birth, int(birth[0]))
                marr_formatted = date(int(marr[2]), month_marr, int(marr[0]))
                if lookupID == wifi:
                    s_type = "wife"
                if lookupID == husi:
                    s_type = "husband"
                us10List.append(
                    [lookupID, str(obirth), str(marr_formatted), s_type, fid])
                # return us05List
            # else: gotmatch = 0; gotdeath = 0

    fcopy.close()
    return us10List


def _us10print(list):

    for x in list:
        print("ERROR: INDIVIDUAL: US10: " + x[0] + " Married " + x[1] + " " +
              x[3] + " (Family: " + x[4] + ") has to be at least 14 to get married")


def _us11(sndmage, divdate, id):
    us11List = []

    if len(sndmage) != 0:
        snd_to_num = abbr_to_num[sndmage[1]]
    if len(divdate) != 0:
        div_to_num = abbr_to_num[divdate[1]]
    if len(sndmage) != 0:
        snd_date = date(int(sndmage[2]), snd_to_num, int(sndmage[0]))
    if len(divdate) != 0:
        div_date = date(int(divdate[2]), div_to_num, int(divdate[0]))
    if len(divdate) == 0:
        s = [id, str(snd_date), '']
        us11List.append(list(s))
        return us11List
    # birth month, divorce month
    # yyyy-mm-dd format

    # find time difference between marriage and divorce
    time_diff = _age(snd_date, div_date)

    if time_diff < 0:

        # return INDI where the 2nd marrigage happens before divorce
        s = [id, str(div_date), str(snd_date)]
        us11List.append(list(s))
    return us11List



def _us12(mm_id, mother_birth, dd_id, father_birth, children_birth):
    # children and parents should be less than 80 years old
    mmn_to_num = abbr_to_num[mother_birth[1]]
    ffn_to_num = abbr_to_num[father_birth[1]]
    mmn_date = date(int(mother_birth[2]), mmn_to_num, int(mother_birth[0]))
    ff_date = date(int(father_birth[2]), ffn_to_num,  int(father_birth[0]))
    mom_age_today = _age(date.today(), mmn_date)
    dad_age_today = _age(date.today(), ff_date)
    if mom_age_today > 80 or dad_age_today > 80:
        return False
    for chil in children_birth:
        cc_to_num = abbr_to_num[chil[1][1]]
        cc_date = date(int(chil[1][2]), cc_to_num, int(chil[1][0]))
        cc_age = _age(date.today(), cc_date)
        if cc_age > 80:
            return False
    return True


def _us28(bdate, id, l):
    bmn_to_num = abbr_to_num[bdate[1]]

    birth_date = date(int(bdate[2]), bmn_to_num, int(bdate[0]))

    l = [{'@I6@:' 'Gordan Ramsley', 'birth:' '2007-3-1'},
         {'@I7@:' 'Morgan Ramsley',  'birth:' '2008-4-1'},
         {'@I8:' 'Rose Chang', 'birth:' '2008-3-21'},
         {'@I9:' 'Astrid Chang', 'birth:' '2008-3-21'}]

    print("ERROR: FAMILY: US28: " + l)


def _us28print(list):

    for x in list:
        print("Error:Individual:US28:" + x[1])


def _us36(ddate, id):

    dmn_to_num = abbr_to_num[ddate[1]]

    death_date = date(int(ddate[2]), dmn_to_num, int(ddate[0]))

    #current_date = date.today().isoformat()
    days_before = (date.today()-timedelta(days=30)).isoformat()

    dead_diff = _age(ddate, days_before)

    if dead_diff < 30:

        s = [id, str(death_date)]
        us36List.append(list(s))
        return us36List



def _us36print(list):

    for x in list:
        print("ERROR: INDIVIDUAL: US36: " + x[2])

    print("ERROR: INDIVIDUAL: US36: Death is more than 30 days")


def _us27(bdate, ddate, tdate, id, name):
    
    birth_date = -1
    given_date = -1
    age_diff = -1
    bmn_to_num = abbr_to_num[bdate[1]]
    
    if tdate == 0:
        # converts month name to a number
        dmn_to_num = abbr_to_num[ddate[1]]
        # yyyy-mm-dd format
        if _us42(int(bdate[2]), bmn_to_num, int(bdate[0])):
            birth_date = date(int(bdate[2]), bmn_to_num, int(bdate[0]))
        else:
            s = [id, 0, int(bdate[2]), bmn_to_num, int(bdate[0])]
            if s in us42List:
                pass
            else:
                us42List.append(s)
        if _us42(int(bdate[2]), bmn_to_num, int(bdate[0])):
            given_date = date(int(ddate[2]), dmn_to_num, int(ddate[0]))
        else:
            s = [id, 0, int(ddate[2]), dmn_to_num, int(ddate[0])]
            if s in us42List:
                pass
            else:
                us42List.append(s)
        
        if (birth_date != -1) and (given_date != -1): 
            age_diff = _age(given_date, birth_date)
        
    elif ddate == 0:
        # yyyy-mm-dd format
        if _us42(int(bdate[2]), bmn_to_num, int(bdate[0])):
            birth_date = date(int(bdate[2]), bmn_to_num, int(bdate[0]))
        else:
            s = [id, 0, int(bdate[2]), bmn_to_num, int(bdate[0])]
            if s in us42List:
                pass
            else:
                us42List.append(s)
        if _us42(int(tdate[0]), int(tdate[1]), int(tdate[2])):
            given_date = date(int(tdate[0]), int(tdate[1]), int(tdate[2]))
        else:
            s = [id, 0, int(tdate[0]), int(tdate[1]), int(tdate[2])]
            if s in us42List:
                pass
            else:
                us42List.append(s)
        # birth_date = date(int(bdate[2]), bmn_to_num, int(bdate[0]))
        # given_date = date(int(tdate[0]), int(tdate[1]), int(tdate[2]))
        
        if (birth_date != -1) and (given_date != -1): 
            age_diff = _age(given_date, birth_date)
    
    if age_diff != -1:
        s = [id, name, str(age_diff)]
        us27List.append(list(s))
    return us27List


def _us27print(list):
    
    for x in list:
        print("LIST: INDIVIDUAL: US27:", x[0] + ":", x[1] + ":", x[2], "years old")


def _us29(id, name):
    
    s = [id, name]
    deadList.append(s)


def _us29print(list):
    
    for x in list:
        print("LIST: INDIVIDUAL: US29:", x[0] + ":", x[1])


def _us42(gyear, gmonth, gdate):
    
    result = True
    
    while True:
        try:
            date(gyear, gmonth, gdate)
            break
        except ValueError:
            result = False
            break

    return result


def _us42print():
    
    for x in us42List:
        if x[1] == 0:
            print("ERROR: INDIVIDUAL: US42:", str(x[0]) + ": Birth", str(x[2]) + "-" + str(x[3]) + "-" + str(x[4]), "does not have a valid date for the given month")
        if x[1] == 1:
            print("ERROR: INDIVIDUAL: US42:", str(x[0]) + ": Death", str(x[2]) + "-" + str(x[3]) + "-" + str(x[4]), "does not have a valid date for the given month")
        if x[1] == 2:
            if str(x[0][1]) == "I":
                print("ERROR: INDIVIDUAL: US42:", str(x[0]) + ": Marriage", str(x[2]) + "-" + str(x[3]) + "-" + str(x[4]), "does not have a valid date for the given month")
            else:
                print("ERROR: FAMILY: US42:", str(x[0]) + ": Marriage", str(x[2]) + "-" + str(x[3]) + "-" + str(x[4]), "does not have a valid date for the given month")
        if x[1] == 3:
            if str(x[0][1]) == "I":
                print("ERROR: INDIVIDUAL: US42:", str(x[0]) + ": Divorce", str(x[2]) + "-" + str(x[3]) + "-" + str(x[4]), "does not have a valid date for the given month")
            else:
                print("ERROR: FAMILY: US42:", str(x[0]) + ": Divorce", str(x[2]) + "-" + str(x[3]) + "-" + str(x[4]), "does not have a valid date for the given month")
                

for line in f:

    token = line.split()  # list of the line
    numtok = len(token)

    if line == "\n":
        continue  # ignore the empty lines

    tok0 = int(token[0])  # first token: level 012

    if (tok0 < 0) or (tok0 > 2):
        continue  # print("Invalid level.") #checks for invalid level

    tok1 = token[1]  # second token: tags

    if tok1 in validtags:  # check if second token is a valid tag
        # if (numtok < 3) and (tok1 not in singletag): continue #only a tag is present, no string        ex: 1 BIRT/MARR/DIV
        # print("todo: " + tok1)

        # #level 0 tags
        # if (tok0 == 0) and (tok1 in tag0): #INDI and FAM does not pass this if statement
        #     print("Debug: Level " + str(tok0) + ", but it's not important.")

        # level 1 tags
        strList = token[2:]
        fullStr = ' '.join(str(i) for i in strList)

        if (tok0 == 1) and (tok1 in tag1):

            if tok1 == "NAME":
                tblx_name = fullStr
            if tok1 == "DIV":
                divfday = 1
            if tok1 == "BIRT":
                birfday = 1
            if tok1 == "DEAT":
                deafday = 1
            if tok1 == "MARR":
                marfday = 1
            if tok1 == "SEX":
                tblx_gend = fullStr
            if tok1 == "FAMC":
                tblx_carr.append(fullStr)
                tblx_chil = tblx_carr
            if tok1 == "FAMS":
                tblx_sarr.append(fullStr)
                tblx_spou = tblx_sarr
            if tok1 == "CHIL":
                tbly_carr.append(fullStr)
                tbly_chil = tbly_carr
                #old_val = fam_id_kids[tbly_id]
                #new_val = old_val + 1
                #fam_id_kids[tbly_id] = new_val
            if tok1 == "WIFE":
                tbly_wifi = fullStr
                matchName = _matchId(tbly_wifi)
                tbly_wifn = matchName
                tbly_sarr.append(fullStr)
            if tok1 == "HUSB":
                tbly_husi = fullStr
                matchName = _matchId(tbly_husi)
                tbly_husn = matchName
                tbly_sarr.append(fullStr)
            
            

        # level 2 tags
        elif (tok0 == 2) and (tok1 in tag2):
            if tok1 == "DATE":

                if birfday == 1:
                    tblx_birt = fullStr
                    birfday = 0

                if deafday == 1:
                    tblx_deat = fullStr
                    deafday = 0
                    tblx_aliv = False

                if marfday == 1:
                    tbly_marr = fullStr
                    marfday = 0

                if divfday == 1:
                    tbly_divo = fullStr
                    divfday = 0

    else:  # check if third token is a valid tag   ex: INDI or FAM

        if numtok < 3:
            continue

        tok2 = token[2]

        if tok2 in extag:
            if tok2 == "INDI":
                if tblx_id != "N/A":

                    # calculate accurate ages
                    today = date.today()
                    today_split = str(today).split("-")
                    birth_split = tblx_birt.split()
                    death_split = tblx_deat.split()
                    # convert month name to number  ex: May -> 5
                    bmn_to_num = abbr_to_num[birth_split[1]]
                    if tblx_aliv == True:
                        if _us42(int(birth_split[2]), bmn_to_num, int(birth_split[0])): 
                            tblx_age = _age(today, date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))
                        else: 
                            s = [tblx_id, 0, int(birth_split[2]), bmn_to_num, int(birth_split[0])]
                            if s in us42List:
                                pass
                            else:
                                us42List.append(s)
                    elif tblx_aliv == False:
                        if _us42(int(birth_split[2]), bmn_to_num, int(birth_split[0])): 
                            dmn_to_num = abbr_to_num[death_split[1]]
                            if _us42(int(death_split[2]), dmn_to_num, int(death_split[0])):
                                tblx_age = _age(date(int(death_split[2]), dmn_to_num, int(death_split[0])), date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))
                            else: 
                                s = [tblx_id, 1, int(death_split[2]), dmn_to_num, int(death_split[0])]
                                if s in us42List:
                                    pass
                                else:
                                    us42List.append(s)
                        else: 
                            s = [tblx_id , 0, int(birth_split[2]), bmn_to_num, int(birth_split[0])]
                            if s in us42List:
                                pass
                            else:
                                us42List.append(s)
                            
                    # call INDI story functions here
                    if tblx_deat != "N/A":
                        if _us42(int(birth_split[2]), bmn_to_num, int(birth_split[0])): 
                            dmn_to_num = abbr_to_num[death_split[1]]
                            if _us42(int(death_split[2]), dmn_to_num, int(death_split[0])):
                                _us03(birth_split, death_split, tblx_id)
                                _us27(birth_split, death_split, 0, tblx_id, tblx_name)
                                _us29(tblx_id, tblx_name)
                            else: 
                                s = [tblx_id, 1, int(death_split[2]), dmn_to_num, int(death_split[0])]
                                if s in us42List:
                                    pass
                                else:
                                    us42List.append(s)
                        else: 
                            s = [tblx_id , 0, int(birth_split[2]), bmn_to_num, int(birth_split[0])]
                            if s in us42List:
                                pass
                            else:
                                us42List.append(s)
                        # _us03(birth_split, death_split, tblx_id)
                        # _us27(birth_split, death_split, 0, tblx_id, tblx_name)
                        # _us29(tblx_id, tblx_name)
                    if tblx_deat == "N/A":
                        _us27(birth_split, 0, today_split, tblx_id, tblx_name)

                    x.add_row([tblx_id, tblx_name, tblx_gend, tblx_birt,
                              tblx_age, tblx_aliv, tblx_deat, tblx_chil, tblx_spou])
                    tblx_id = "N/A"
                    tblx_name = "N/A"
                    tblx_gend = "N/A"
                    tblx_birt = "N/A"
                    tblx_age = "N/A"
                    tblx_aliv = "N/A"
                    tblx_deat = "N/A"
                    tblx_chil = "N/A"
                    tblx_spou = "N/A"
                    tblx_carr = []
                    tblx_sarr = []
                    tblx_id = tok1
                    tblx_aliv = True

                elif tblx_id == "N/A":

                    tblx_id = tok1
                    tblx_aliv = True

            if tok2 == "FAM":
                

                marr_split = tbly_marr.split()
                divo_split = tbly_divo.split()

                if tbly_id != "N/A":

                    # call FAM story functions here
                    if tbly_divo != "N/A":
                        _us04(marr_split, divo_split, tbly_id)
                        _us06(tbly_sarr, tbly_divo, tbly_wifi, tbly_husi, tbly_id)
                    if tbly_marr != "N/A":
                        _corpseBride(tbly_sarr, tbly_marr,
                                     tbly_wifi, tbly_husi, tbly_id)
                        _us10(tbly_sarr, tbly_marr,
                              tbly_wifi, tbly_husi, tbly_id)

                    y.add_row([tbly_id, tbly_marr, tbly_divo, tbly_husi,
                              tbly_husn, tbly_wifi, tbly_wifn, tbly_chil])
                   #_us09(tbly_id,tbly_carr)
                    #print(tbly_carr)
                   
                    tbly_id = "N/A"
                    tbly_marr = "N/A"
                    tbly_divo = "N/A"
                    tbly_husi = "N/A"
                    tbly_husn = "N/A"
                    tbly_wifi = "N/A"
                    tbly_wifn = "N/A"
                    tbly_chil = "N/A"
                    tbly_carr = []
                    tbly_sarr = []
                    tbly_id = tok1

                elif tbly_id == "N/A":
                    tbly_id = tok1
                   

        else:
            continue
            # print("Invalid tag as 3rd token")

today = date.today()
birth_split = tblx_birt.split()
death_split = tblx_deat.split()
marr_split = tbly_marr.split()
divo_split = tbly_divo.split()
bmn_to_num = abbr_to_num[birth_split[1]]

if tblx_aliv == True:
    if _us42(int(birth_split[2]), bmn_to_num, int(birth_split[0])): 
        tblx_age = _age(today, date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))
    else: 
        s = [tblx_id, 0, int(birth_split[2]), bmn_to_num, int(birth_split[0])]
        if s in us42List:
            pass
        else:
            us42List.append(s)
elif tblx_aliv == False:
    if _us42(int(birth_split[2]), bmn_to_num, int(birth_split[0])): 
        dmn_to_num = abbr_to_num[death_split[1]]
        if _us42(int(death_split[2]), dmn_to_num, int(death_split[0])):
            tblx_age = _age(date(int(death_split[2]), dmn_to_num, int(death_split[0])), date(int(birth_split[2]), bmn_to_num, int(birth_split[0])))
        else: 
            s = [tblx_id, 1, int(death_split[2]), dmn_to_num, int(death_split[0])]
            if s in us42List:
                pass
            else:
                us42List.append(s)
    else: 
        s = [tblx_id , 0, int(birth_split[2]), bmn_to_num, int(birth_split[0])]
        if s in us42List:
            pass
        else:
            us42List.append(s)
            
# call ALL story functions here
if tblx_deat != "N/A":
    if _us42(int(birth_split[2]), bmn_to_num, int(birth_split[0])): 
        dmn_to_num = abbr_to_num[death_split[1]]
        if _us42(int(death_split[2]), dmn_to_num, int(death_split[0])):
            _us03(birth_split, death_split, tblx_id)
            _us27(birth_split, death_split, 0, tblx_id, tblx_name)
            _us29(tblx_id, tblx_name)
        else: 
            s = [tblx_id, 1, int(death_split[2]), dmn_to_num, int(death_split[0])]
            if s in us42List:
                pass
            else:
                us42List.append(s)
    else: 
        s = [tblx_id , 0, int(birth_split[2]), bmn_to_num, int(birth_split[0])]
        if s in us42List:
            pass
        else:
            us42List.append(s)
    # _us03(birth_split, death_split, tblx_id)
    # _us27(birth_split, death_split, 0, tblx_id, tblx_name)
if tblx_deat == "N/A":
    _us27(birth_split, 0, today_split, tblx_id, tblx_name)
if tbly_divo != "N/A":
    _us04(marr_split, divo_split, tbly_id)
if tbly_marr != "N/A":
    _corpseBride(tbly_sarr, tbly_marr, tbly_wifi, tbly_husi, tbly_id)
    _us10(tbly_sarr, tbly_marr, tbly_wifi, tbly_husi, tbly_id)

x.add_row([tblx_id, tblx_name, tblx_gend, tblx_birt, tblx_age,
          tblx_aliv, tblx_deat, tblx_chil, tblx_spou])
_us15(tbly_id, tbly_chil)
y.add_row([tbly_id, tbly_marr, tbly_divo, tbly_husi,
          tbly_husn, tbly_wifi, tbly_wifn, tbly_chil])

print("Individuals")
print(x.get_string(sortby="ID"))
print("Families")
print(y.get_string(sortby="ID"))

print("\n")
_us03print(us03List)
_us04print(us04List)
_us05print(us05List)
_us06print(us06List)
_us07Aprint(us07ListA)
_us07bprint(us07ListB)
_us10print(us10List)
_us36print(us36List)
_us27print(us27List)
_us28print(us28List)
_us29print(deadList)
_us42print()

f.close()