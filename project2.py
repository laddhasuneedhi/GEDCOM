'''

SSW555 Project 2: GEDCOM
Ali El Sayed
I pledge my honor that i have abided by the stevens honor system

'''
from prettytable import PrettyTable
import sys
import os

if len(sys.argv) == 1:
	print ("\nPlease provide input filename as the first argument and try again.\n")
	quit()

arg_0 = sys.argv[0] #python sourcefile
arg_1 = sys.argv[1] #input filename

currpath = os.getcwd()
print(currpath)
outputpath = str(currpath) + "\\outputP2.txt"   #gets path for output file

"""
def answer():
    '''takes file and transforms it'''
    level0a = ['NOTE', 'HEAD', 'TRLR']
    level0b = ['FAM', 'INDI']
    remainLevels = ['NAME', 'SEX', 'DATE', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']

    # file = open("/Users/alielsayed/Fall '22/CS555/CS555 GEDCOM2 Ali_E/CS555 M1B1 Project1GEDCOM", 'r')
    file = open(arg_1, 'r')

    for line in file:
        # with open("/Users/alielsayed/Fall '22/CS555/CS555 GEDCOM2 Ali_E/outputP2.txt", "a") as f:
        with open(outputpath, 'a') as f:
            print(' ', file =f)
            print('--> ' + line, file =f) #print line
            slots = line.split()
            level = slots[0]
            tag = slots[1]
            argsList = slots[2:]
            arguments = ' '.join(str(i) for i in argsList) 

            newLine = '<-- ' + level + '|'
            
            #if level is 0
            if(level == '0'):
                lineZero = ''
                if (tag in level0a):
                    lineZero = tag + '|Y|' + arguments
                elif (tag in level0b):
                    lineZero = arguments + '|Y|' + tag
                else:
                    lineZero = tag + '|N|' + arguments
                answerZero = newLine + lineZero
                print(answerZero, file =f)

            #if level is 1 or 2
            if(level == '1' or level == '2'):
                lineOne = ''
                if (tag in remainLevels):
                    lineOne  = tag + '|Y|' + arguments
                else:
                    lineOne = tag + '|N|' + arguments
                answerOne = newLine + lineOne
                print(answerOne, file =f)

answer()

# """