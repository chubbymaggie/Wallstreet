'''
Created on 13.10.2013

@author: Marion
'''

import re


class Info(object):
    '''
    INFO CLASS
    
    does all the info gathering out of the database
    stupid name i know
    '''


    def __init__(self):
        import Database.SQLiteDB
        self.db = Database.SQLiteDB.SQLiteDB()
        
        
    ###
    # search functions return cursors
    # diff functions create/open csv files
    # oh i like defining rules..
    ###
        
    def search_libs(self, libname):
        ids = self.db.select_libs_byname(libname) # libid, libname, os, filetype
        return ids
        
        #for item in ids:
        #    print "Library ID %s for %s with type %s and OS %s" % (item[0], item[1], item[3], item[2])
    
    
    def search_libs_diffing(self, libname):
        cur = self.db.select_libs_byname(libname)
        ids = cur.fetchall()    # without fetch the rowcount is always -1
        wids = []

        # works only for Win7/Win8 diffing !!
        if len(ids) == 2:
            if (ids[0][3].lower() == ids[1][3].lower()): #filetype
                if (ids[0][2] != ids[1][2]):
                    if (ids[0][2] == 'WIN7'): #os
                        wids.append(ids[0][0]) #id
                    elif (ids[1][2] == 'WIN7'): #os
                        wids.append(ids[1][0]) #id
                    else:
                        return -1
                    
                    if (ids[0][2] == 'WIN8'):
                        wids.append(ids[0][0])
                    elif (ids[1][2] == 'WIN8'):
                        wids.append(ids[1][0])
                    else:
                        return -1
                    
                    return wids
                else:
                    return -1
            else:
                return -1
        else:
            return -1


    # DEPRECATED
    def diff_libs(self, w7lib, w8lib):
        
        cur_one = self.db.select_diff_one(w8lib) # sigpattern,  funcname, count(*) co
        res = cur_one.fetchall()
         
        print "Function_Name;Pattern;Win8_Hits;Win7_Hits"

        for item in res:
            fsplit = re.split('\(', item[1], 1, 0) #funcname
            
            cur_two = self.db.select_diff_two(w7lib,item[0],fsplit[0]) # sigpattern
            hitcount_two = cur_two.fetchone()
             
            if hitcount_two:
                print "%s;%s;%s;%s" % (fsplit[0],item[0],item[2],hitcount_two[2]) #sigpattern, co
            elif (self.db.select_function(fsplit[0], w7lib)):
                print "%s;%s;%s;0" % (fsplit[0],item[0],item[2]) #sigpattern, co
            else:
                print "%s;%s;%s;func_non_existent" % (fsplit[0],item[0],item[2]) #sigpattern, co
        

    # returns TEXT
    def diff_twosided(self, w7lib, w8lib):

        cur_one = self.db.select_diff_one(w8lib) # sigpattern,  funcname, count(*) co
        res = cur_one.fetchall()
         
        output = "Function_Name;Pattern;Win8_Hits;Win7_Hits\n"

        for item in res:
            fsplit = re.split('\(', item[1], 1, 0) #funcname
            
            cur_two = self.db.select_diff_two(w7lib,item[0],fsplit[0]) #sigpattern
            hitcount_two = cur_two.fetchone()
             
            if (hitcount_two):
                if item[2] != hitcount_two[0]: #count
                    output += "%s;%s;%s;%s\n" % (fsplit[0],item[0],item[2],hitcount_two[0]) # sigpattern, co, co

            elif (self.db.select_function(fsplit[0], w7lib)):
                output += "%s;%s;%s;0\n" % (fsplit[0],item[0],item[2]) # sigpattern, co

        output += "\nFunction_Name;Pattern;Win7_Hits;Win8_Hits\n"
        
        cur_one = self.db.select_diff_one(w7lib) # sigpattern,  funcname, count(*) co
        res = cur_one.fetchall()
         
        for item in res:
            fsplit = re.split('\(', item[1], 1, 0) # funcname
            
            cur_two = self.db.select_diff_two(w8lib,item[0],fsplit[0])
            hitcount_two = cur_two.fetchone()
             
            if (hitcount_two):
                if item[2] != hitcount_two[0]: # co
                    output += "%s;%s;%s;%s\n" % (fsplit[0],item[0],item[2],hitcount_two[0])

            elif (self.db.select_function(fsplit[0], w8lib)):
                output += "%s;%s;%s;0\n" % (fsplit[0],item[0],item[2])
                
        return output

    def library_info(self,libid):    
        cur_all = self.db.select_lib_all(libid) # libname, funcname, sigpattern, line_offset
        return cur_all

    # only CMDLine version
    def print_mappings(self):
        cur_all = self.db.select_mappings()
        print "Sigpattern;Mapping"
        for item in cur_all:
            print "%s;%s" % (item[0],item[1])
            
            