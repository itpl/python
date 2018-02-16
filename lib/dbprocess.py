#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Program: order execute V1.0
# Author:  Clumart.G(翅儿学飞)
# Date:    2018-02-12
# Update:  2018021201 None

#Build-in Module
import os
import sys
import string
import time

#Third Part Module
import pymysql 

#Project Module
file_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_path)
home_dir = os.path.dirname(file_dir)

sys.path.append(home_dir+"/lib/")
import loadconf
import log 

#Project code
class DatabaseProcess():
    '''Database opration process.'''
     
    def __init__(self):
        '''
        Summary: Class init. 
        @param type name des
        '''
        #read config
        conf = loadconf.GetConfig()
        self.db_host = ("mysql_db_host" in conf.conf and conf.conf["mysql_db_host"] or "127.0.0.1")
        self.db_port = ("mysql_db_port" in conf.conf and int(conf.conf["mysql_db_port"]) or 3306)
        self.db_user = ("mysql_db_user" in conf.conf and conf.conf["mysql_db_user"] or "root")
        self.db_pass = ("mysql_db_pass" in conf.conf and conf.conf["mysql_db_pass"] or "")
        self.db_name = ("mysql_db_name" in conf.conf and conf.conf["mysql_db_name"] or "")
        
        #db config 
        self.db_char = "utf8"
        self.db_size = 16*1024*1024
        self.db_time = 30
        self.db_auto = False
         
        #log
        self.ilog = log.LogRecord()
        
    def dbconn(self, database = ""):
        '''
        Summary:Database connect.
        
        Description:Connect to database, defaut database use the config db_name,
                    you can set it by prarm.
         
        @param  string  database    the database connect 
        @return None
         
        '''
        if not database:
            database = self.db_name
         
        self.db_conn = pymysql.connect(host = self.db_host, 
                                  port = self.db_port, 
                                  user = self.db_user,
                                  password = self.db_pass,
                                  database = self.db_name,
                                  charset = self.db_char,
                                  max_allowed_packet = self.db_size,
                                  connect_timeout = self.db_time,
                                  autocommit = self.db_auto 
                                  )
        
        self.db_conn.select_db(database)
        self.db_conn.autocommit_mode = False
    
    def dbdisconn(self, conn = ""):
        '''
        Summary:Database disconnect.
        
        Description:Close connection of database.
         
        @param  class   the database connection
        @return None
         
        '''
        if not conn:
            self.db_conn.close()
        else:
            conn.close()
         
    def get_records_base(self, co=None, tb=None, wh=None, od=None, li=None):
        '''
        Summary:get data from database 
        
        Description:get some data from table, it's can be one or someone.
         
        @param  list    co  columns to show
        @param  string  tb  the table
        @param  dict|string wh  the where condition:dict mean "k1=v1 and k2=v2" or use string mean your own where condition
        @param  list    od  order by [ column, asc/desc ]
        @param  list    li  limit [ start, end ]
        @return dict        the numbers inserted 
         
        '''
         
        #db conn
        if not hasattr(self, "db_conn"):
            self.dbconn()
        db_conn = self.db_conn
         
        with db_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Read a single record
            #select a,b...
            sql_columns = "SELECT "
            if co:
                for v in co:
                    if sql_columns == "SELECT ":
                        sql_columns = sql_columns+v
                    else:
                        sql_columns = sql_columns+","+v
            else:
                sql_columns = sql_columns+" * "
                 
            #from table
            sql_table = " FROM `"+tb+"` "
             
            #where k=v and ...
            if not wh:
                sql_where = " "
            else:
                sql_where = " WHERE "
                if type(wh) == str:
                    sql_where = sql_where+wh
                else:
                    for k,v in wh.items():
                        if v == True:
                            v=1
                        if v == False:
                            v=0
                        if type(v) == str:
                            v = "\""+v+"\""
                        else:
                            v = str(v)
                        if sql_where == " WHERE ":
                            sql_where = sql_where+k+"="+v
                        else:
                            sql_where = sql_where+" and "+k+"="+v
            #order by 
            if not od:
                sql_order = " "
            else:
                sql_order = " order by "
                for v in od:
                    sql_order = sql_order+" "+v
            #limit startpos, length
            if not li:
                sql_limit = " "
            else:
                sql_limit = " limit "
                for v in li:
                    if sql_limit == " limit ":
                        sql_limit = sql_limit+v
                    else:
                        sql_limit = sql_limit+","+v
                         
            #run sql and get result
            self.ilog.log_write("main", "debug", sql_columns+sql_table+sql_where+sql_order+sql_limit)
            cursor.execute(sql_columns+sql_table+sql_where+sql_order+sql_limit)
            result = cursor.fetchall()
        
        return result
        
    def order_insert(self, data):
        '''
        Summary:Insert data to table orders
        
        Description:Insert some data to table orders, it's can be one or someone.
         
        @param  list    data    the data need to insert,data should dict, every data in lists
        @return dict            the numbers inserted 
         
        '''
         
        #db conn
        if not hasattr(self, "db_conn"):
            self.dbconn()
        db_conn = self.db_conn
         
        try:
            db_conn.begin()
            with db_conn.cursor() as cursor:
                for v in data:
                    #data check and format
                    if not v["user"]:
                        v["user"] = "NULL" 
                    else:
                        v["user"] = "\""+str(v["user"])+"\""
                         
                    # Create sql stru 
                    sql = "INSERT INTO `user` (`user`\
                                               ) VALUES ('"\
                                               +v['user']+"'"\
                                               +")"
                    self.ilog.log_write("main", "debug", sql)
                    cursor.execute(sql)
                      
            # sql commit or db_conn.rollback()
            db_conn.commit()
        finally:
            return None 
              
#Run myself
if __name__ == '__main__':
    #a = DatabaseProcess()
    #d = [{"user":"zhangshan"}, {"user":"lisi"}]
    #a.order_insert(d)
    #print(a.get_records_base(["id", "user"], "user", None, ["id", "desc"], None))
    #a.dbdisconn("")
