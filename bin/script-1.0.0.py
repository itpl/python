#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Program: Script V1.0
# Author:  Clumart.G(翅儿学飞)
# Date:    2014-12-12
# Update:  2014121201 None
#Build-in Module
import os
import sys
import string

#Third Part Module

#Project Module
file_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_path)
home_dir = os.path.dirname(file_dir)

sys.path.append(home_dir+"/lib/")
import loadconf 

class SoftInfo():
    '''Show infomation of this software.'''
     
    def __init__(self,softname,softversion):
        self.softname = softname
        self.softversion = softversion
    
    def info_head(self):
        '''The header of software message(s)'''
        print(" o----------------------------------------------------------------o")
        print(" | :: %-35s    %20s |" % (self.softname,"V "+self.softversion))
        print(" o----------------------------------------------------------------o")
    
    def info_start(self):
        os.system("clear")
        '''Show the message when the beginning of this software.'''
        self.info_head() 
        
        print(" |                                                                |")
        print(" |                Thank you for use this script!                  |")
        print(" |                                                                |")
        print(" |                     http://www.idcsrv.com                      |")
        print(" |                                                                |")
        print(" |                   Author:翅儿学飞(Clumart.G)                   |")
        print(" |                    Email:myregs6@gmail.com                     |")
        print(" |                         QQ:1810836851                          |")
        print(" |                         QQ群:61749648                          |")
        print(" |                                                                |")
        print(" |          Hit [ENTER] to continue or ctrl+c to exit             |")
        print(" |                                                                |")
        print(" o----------------------------------------------------------------o")
        input()
        os.system("clear")
        
    def info_end(self):
        '''Show the message when the end of this software.'''
        self.info_head();
        print(" |                                                                |")
        print(" |                       Congratulations :)                       |")
        print(" |                                                                |")
        print(" |                The software has been installed!                |")
        print(" |                                                                |")
        print(" |                     http://www.idcsrv.com                      |")
        print(" |                                                                |")
        print(" |                   Author:翅儿学飞(Clumart.G)                   |")
        print(" |                    Email:myregs6@gmail.com                     |")
        print(" |                         QQ:1810836851                          |")
        print(" |                         QQ群:61749648                          |")
        print(" |                                                                |")
        print(" o----------------------------------------------------------------o")

    def info_err_head(self):
        '''The header of error message(s)'''
        print(" o----------------------------------------------------------------o")
        print(" | :: %-35s    %20s |" % ("Error","V "+self.softversion))
        print(" o----------------------------------------------------------------o")
    
    def info_err_info(self,errmsg):
        '''Show the error message(s)'''
        self.info_err_head()
        print("Error Message:")
        print("%s " %(errmsg))

class ThisIsAClass():
    '''Class Commit'''
     
    def __init__(self):
        print("Class Example!")
    
    def function_name(self):
        print(self.__class__.__name__)

if __name__ == '__main__':
    ShowSoftInfo = SoftInfo("ScriptName","1.0.15-beta")
    ShowSoftInfo.info_start()
    ShowSoftInfo.info_err_info("error test\nerror test infomation")
    ShowSoftInfo.info_end()
    #LogRecore("default.log");
    a = loadconf.GetConfig();
    print(a.conf);
