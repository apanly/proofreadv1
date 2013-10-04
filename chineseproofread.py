#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
import os
import sys
import json
from checkproof import proofcheck

class proofread:
    def __init__(self):
        if os.path.exists("dicmap.txt"):
            encodedjson=self.readfile()
            self.dicmap=json.loads(encodedjson)
        else:
            self.dicmap=self.initdicmap()
        for item in self.dicmap:
            #print "%s:%d"%(item,self.dicmap[item])
            print item
        exit

    def proofreadAndSuggest(self,txt):
        ctarget=proofcheck(self.dicmap)
        ctarget.proofreadAndSuggest(u"%s"%txt)

    def initdicmap(self):
        root='dataset2/'
        list=os.listdir(root)
        tmplines=[]
        maplist={}
        for d in list:
            dir = os.listdir(root+d+"/")
            for f in dir:
                file=open(root+d+"/"+f)
                while 1:
                    lines = file.readlines(100000)
                    if not lines:
                        break
                    for line in lines:
                        tmplines.append(line)
        for line in tmplines:
            line=self.filter(line)
            ret=jieba.cut(line,cut_all=False)
            tmplitter=[]
            littercnt=0
            indexf=0
            for item in ret:
                tmplitter.append(self.filter(item))
                littercnt+=1
            for litter in tmplitter:
                if litter and type(litter) is not int:
                    if litter in maplist:
                        maplist[litter]+=1
                    else:
                        maplist[litter]=1
                    #if  indexf<littercnt-1:
                    #    if tmplitter[indexf+1] and type(tmplitter[indexf+1]) is not int:
                    #        tmpanotherlitter=litter+tmplitter[indexf+1]
                    #        if tmpanotherlitter in maplist:
                    #            maplist[tmpanotherlitter]+=1
                    #        else:
                    #            maplist[tmpanotherlitter]=1
                #indexf+=1
        encodedjson = json.dumps(maplist)
        self.writefile(encodedjson)
        return maplist

    def writefile(self,txt):
        file_object = open('dicmap.txt', 'w')
        file_object.write(txt)
        file_object.close()

    def readfile(self):
        file_object = open('dicmap.txt', 'r')
        txt=file_object.read( )
        file_object.close()
        return txt


    def filter(self,line):
        spechars=[",",":",'"',"'","﹔","ㄍ","#","\\","）","（","，","！",".","-","/","’","，","？","?","[","；","）",")","(","，","。","、","“","，","%","·","》","”","*",">","┆","：","．","％","】","《","]","_","〗","【","██","|","]","}","="]
        line=line.strip()
        for spechar in spechars:
            line=line.replace(spechar,"")
        line=line.strip()
        return line