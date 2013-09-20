#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from chineseproofread import proofread
from checkproof import proofcheck

def main():
    ptarget=proofread()
    ptarget.proofreadAndSuggest("天汽")

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()



