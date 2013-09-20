#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
class proofcheck:
    def __init__(self,maplist):
        self.maplist=maplist
        pass
    def proofreadAndSuggest(self,txt):
        sInputResult=list(txt)
        correctTokens,errorTokens=self.getCorrectTokens(sInputResult)
        #我个人觉得只要找出错了就好了，对的没有必要要把
        if len(errorTokens)>0:
            ret=jieba.cut(txt,cut_all=False)
            unitresult=[]
            for unittoken in ret:
                if len(errorTokens)>0:
                    for errortoken in errorTokens:
                        if errortoken in unittoken:
                            unitresult.append(unittoken.replace(errortoken,""))
                            errorTokens.remove(errortoken)
                            break
                        else:
                            unitresult.append(unittoken)
                else:
                    unitresult.append(unittoken)

            ctokens=self.readfile()
            for linetoken in ctokens:
                existflag=0
                matchflag=-1
                for unittoken in unitresult:
                    if unittoken  in linetoken:
                        tmpposition=linetoken.find(unittoken)
                        if tmpposition>matchflag:
                            matchflag=tmpposition
                        else:
                            existflag=1
                            break;
                    else:
                        existflag=1
                        break;
                if existflag==0:
                    print linetoken
        else:
            print txt



    #目前先不用，感觉这中算法没什么用处
    def getMaxAndSecondMaxSequnce(self,sInputResult):
        correctTokens,errorTokens=self.getCorrectTokens(sInputResult)
        littleword=''
        maxAndSecondMaxSeq=[0,0]
        correctcount=len(correctTokens)
        if correctcount==0:
            return None
        elif correctcount==1:
            maxAndSecondMaxSeq[0]=correctTokens[0]
            maxAndSecondMaxSeq[1]=correctTokens[0]
            return maxAndSecondMaxSeq
        maxSequence=correctTokens[0]
        maxSequence2=correctTokens[correctcount-1]
        for token in correctTokens:
            if len(token) > len(maxSequence):
                maxSequence = token
            elif len(token) == len(maxSequence):
                if len(token)==1:
                    if self.probBetweenTowTokens(token) > self.probBetweenTowTokens(maxSequence):
                        maxSequence2 = token
                elif len(token)>1:
                    if self.probBetweenTowTokens(token) <= self.probBetweenTowTokens(maxSequence):
                        maxSequence2 = token

            elif len(token) >len(maxSequence2):
                maxSequence2 = token
            elif len(token) == len(maxSequence2):
                if self.probBetweenTowTokens(token) > self.probBetweenTowTokens(maxSequence2):
                    maxSequence2 = token

        #//delete the sub-word from a string
        if len(maxSequence2) == len(maxSequence):
            maxseqvaluableTokens = len(maxSequence)
            maxseq2valuableTokens = len(maxSequence2)
            min_truncate_prob_a = 0
            min_truncate_prob_b = 0
            aword = ""
            bword = ""
            for token in correctTokens:
                tokenprob = self.probBetweenTowTokens(token)
                if maxSequence!=token and  token in maxSequence:
                    if tokenprob >= min_truncate_prob_a:
                        min_truncate_prob_a = tokenprob
                        aword = token
                elif maxSequence2!=token  and token in maxSequence2:
                    if tokenprob >= min_truncate_prob_b:
                        min_truncate_prob_b = tokenprob
                        bword = token
            if len(aword)>0 and  min_truncate_prob_a < min_truncate_prob_b:
                maxseqvaluableTokens -= 1
                littleword = maxSequence.replace(aword,"")
            else:
                maxseq2valuableTokens -= 1
                temp = maxSequence2
                if temp.replace(bword, "") in maxSequence:
                    littleword =  maxSequence2
                else:
                    littleword =  maxSequence2.replace(bword,"")

            if maxseqvaluableTokens < maxseq2valuableTokens:
                maxSequence = maxSequence2
                maxSequence2 = littleword
            else:
                maxSequence2 = littleword

        maxAndSecondMaxSeq[0] = maxSequence
        maxAndSecondMaxSeq[1] = maxSequence2
        return maxAndSecondMaxSeq


    def getCorrectTokens(self,sInputResult):
        correctTokens=[]
        isCorrect=[]
        errorTokens=[]
        hasError = 0
        wrongcnt=0
        for token in sInputResult:
            probOne=self.probBetweenTowTokens(token)
            if probOne<=0:
                isCorrect.append(0)
                wrongcnt+=1
            else:
                isCorrect.append(1)
        tokencount=len(sInputResult)
        #if tokencount>2:
        if tokencount>0:
            if wrongcnt==0:
                counti=0
                while counti<tokencount-1:
                    tokenbuf=sInputResult[counti]
                    countj=counti+1
                    while countj<tokencount:
                        probOne=self.probBetweenTowTokens("%s%s"%(tokenbuf,sInputResult[countj]))
                        if probOne>0:
                            tokenbuf="%s%s"%(tokenbuf,sInputResult[countj])
                        else:
                            if countj<tokencount-1 and self.probBetweenTowTokens("%s%s%s"%(tokenbuf,sInputResult[countj],sInputResult[countj+1]))>0:
                                tokenbuf="%s%s"%(sInputResult[countj],sInputResult[countj+1])
                            else:
                                hasError=1
                                break
                        countj+=1
                    counti+=1
                    correctTokens.append(tokenbuf)
                if self.probBetweenTowTokens(sInputResult[tokencount-1])>0:
                    correctTokens.append(sInputResult[tokencount-1])
            else:
                counti=0
                while counti<tokencount:
                    a=isCorrect[counti]
                    tokenbuf=''
                    if a>0:
                        tokenbuf=sInputResult[counti]
                        countj=counti+1
                        while countj<tokencount:
                            probOne=self.probBetweenTowTokens("%s%s"%(tokenbuf,sInputResult[countj]))
                            if probOne>0:
                                tokenbuf=sInputResult[countj]
                            else:
                                hasError=2
                                break
                            countj+=1
                        correctTokens.append(tokenbuf)
                    elif self.probBetweenTowTokens("%s%s"%(sInputResult[counti],sInputResult[counti+1]))>0:
                        tokenbuf="%s%s"%(sInputResult[counti],sInputResult[counti+1])
                        countj=counti+2
                        while countj<tokencount:
                            probOne=self.probBetweenTowTokens("%s%s"%(tokenbuf,sInputResult[countj]))
                            if probOne>0:
                                tokenbuf="%s%s"%(tokenbuf,sInputResult[countj])
                            else:
                                hasError=3
                                break
                            countj+=1
                        correctTokens.append(tokenbuf)
                    else:
                        hasError=4
                    counti+=1
        #elif tokencount==2:
        #    probOne=self.probBetweenTowTokens("%s%s"%(sInputResult[0],sInputResult[1]))
        #    if probOne>0:
        #        correctTokens.append("%s%s"%(sInputResult[0],sInputResult[1]))

        #计算错误的是哪个地方
        if tokencount>2:
            counti=0;
            while counti<tokencount:
                if counti>0 and counti<tokencount-1:
                    probOnea=self.probBetweenTowTokens("%s%s"%(sInputResult[counti],sInputResult[counti+1]))
                    probOneb=self.probBetweenTowTokens("%s%s"%(sInputResult[counti-1],sInputResult[counti]))
                    if probOnea==0 and probOneb==0:
                        errorTokens.append(sInputResult[counti])
                counti+=1
        elif tokencount==2:
            probOne=self.probBetweenTowTokens("%s%s"%(sInputResult[0],sInputResult[1]))
            if probOne==0:
                errorTokens.append(sInputResult[1])
        return correctTokens,errorTokens


    def readfile(self):
        tmplines=[]
        file = open('correct', 'r')
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                tmplines.append(line)
        return tmplines

    def probBetweenTowTokens(self,token):
        tmpcount=0
        if token in self.maplist:
            tmpcount=self.maplist[token]
        return tmpcount