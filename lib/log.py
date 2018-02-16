#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Program: log recode 
# Author:  Clumart.G(翅儿学飞)
# Date:    2014-05-12
# Update:  2014051201 None

#Build-in Module
import os
import string
import logging
import logging.handlers
import datetime

#Third Part Module

#Project Module

file_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_path)
home_dir = os.path.dirname(file_dir)
log_dir = home_dir+"/var/log" 

import loadconf

class LogRecord():
    '''Log Module.'''
     
    def __init__(self):
        '''set log file path ,load all the settings'''
        
        #load config from etc/main.conf
        cf = loadconf.GetConfig()
        #Main Log File Check
        config_file = "log_main_file" in cf.conf and cf.conf["log_main_file"] or "main.log"
        #get the config file path
        config_file = config_file.strip().lower();
        if config_file[0:1] == "/":
            conf_file_path = config_file;
        else:
            conf_file_path = log_dir+"/"+config_file;
        
        #check log file is exists ,and create it if not.
        if not os.path.isfile(conf_file_path):
            conf_dir_path = os.path.dirname(conf_file_path);
            if not os.path.exists(conf_dir_path):
                os.makedirs(conf_dir_path)
            open(conf_file_path,"w").write("") 
             
        #file read/write check.
        if not os.access(conf_file_path, os.W_OK):
            try:
                os.chmod(conf_file_path, stat.S_IWUSR)
                os.chmod(conf_file_path, stat.S_IWGRP)
                os.chmod(conf_file_path, stat.S_IWOTH)
                self.main_file = conf_file_path
            except IOError as e:
                print("[WARNING] : File Exists but can't access.Error message:"+e.message)
        else:
            self.main_file = conf_file_path
         
        # Error File Check
        error_file = "log_error_file" in cf.conf and cf.conf["log_error_file"] or "main.log"
        #get the config file path
        config_file = error_file.strip().lower();
        if config_file[0:1] == "/":
            conf_file_path = config_file;
        else:
            conf_file_path = log_dir+"/"+config_file;
        
        #check log file is exists ,and create it if not.
        if not os.path.isfile(conf_file_path):
            conf_dir_path = os.path.dirname(conf_file_path);
            #print(conf_file_path);
            #print(conf_dir_path);
            if not os.path.exists(conf_dir_path):
                os.makedirs(conf_dir_path)
            open(conf_file_path,"w").write("") 
             
        #file read/write check.
        if not os.access(conf_file_path, os.W_OK):
            try:
                os.chmod(conf_file_path, stat.S_IWUSR)
                os.chmod(conf_file_path, stat.S_IWGRP)
                os.chmod(conf_file_path, stat.S_IWOTH)
                self.error_file = conf_file_path
            except IOError as e:
                print("[WARNING] : File Exists but can't access.Error message:"+e.message)
        else:
            self.error_file = conf_file_path
        #log level default
        log_level = "log_log_level" in cf.conf and cf.conf["log_log_level"] or "WARNING"
        self.log_level = log_level.strip().upper();
        main_format = "log_main_format" in cf.conf and cf.conf["log_main_format"] or ""
        self.main_format = main_format.strip().lower();
        error_format = "log_error_format" in cf.conf and cf.conf["log_error_format"] or ""
        self.error_format = error_format.strip().lower();
        
    def log_create(self, log_name="root"):
        '''
        Summarg: Create a loger.
        
        Description:
         
        @param  string  log_name    The logger name.
        @return None
        '''
        self.ilog = logging.getLogger(log_name)
        if self.log_level=="CRITICAL":
            self.ilog.setLevel(logging.CRITICAL) 
        elif self.log_level=="ERROR":
            self.ilog.setLevel(logging.ERROR) 
        elif self.log_level=="WARNING":
            self.ilog.setLevel(logging.WARNING) 
        elif self.log_level=="INFO":
            self.ilog.setLevel(logging.INFO) 
        elif self.log_level=="DEBUG":
            self.ilog.setLevel(logging.DEBUG) 
        else: 
            self.ilog.setLevel(logging.WARNING) 
         
        main_handler = logging.handlers.TimedRotatingFileHandler(self.main_file, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        main_handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s]:%(message)s"))
        error_handler = logging.FileHandler(self.error_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s]:%(message)s"))
         
        self.ilog.addHandler(main_handler)
        self.ilog.addHandler(error_handler)
         
    def log_write(self, log_type=None, log_msg_level=None, log_msg = ""):
        '''
        Summarg: Create a loger.
        
        Description:
         
        @param  string  log_name    The logger name.
        @return None
        '''
        if not hasattr(self, "ilog"):
            self.log_create()
        
        if not log_type :
            log_type = "main";
        log_type = log_type.strip().lower()
        if not log_msg_level:
            log_msg_level = "INFO";
        log_msg_level = log_msg_level.strip().upper()
        
        if log_msg_level=="CRITICAL":
            self.ilog.critical(log_msg) 
        elif log_msg_level=="ERROR":
            self.ilog.error(log_msg) 
        elif log_msg_level=="WARNING":
            self.ilog.warning(log_msg) 
        elif log_msg_level=="INFO":
            self.ilog.info(log_msg) 
        elif log_msg_level=="DEBUG":
            self.ilog.debug(log_msg) 
        else: 
            self.ilog.info(log_msg) 
         
if __name__ == '__main__':
    a=LogRecord()
    a.log_write("main", "info", "info msg")
    a.log_write("main", "warning", "warning msg")
    a.log_write("main", "debug", "debug msg")
    a.log_write("main", "CRITICAL", "critical msg")
    a.log_write("main", "ERROR", "debug msg")
