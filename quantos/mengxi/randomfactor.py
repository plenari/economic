#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np #line:6
import pandas as pd #line:7
basic_list =['open/close','rank(volume)','((close-open) / open)','rank((close-avg))','delta(close, 1)','delta(volume, 3)','sign(delta(volume, 1))','((high + low)/2)','((close-low)-(high-close))/(close-low)','rank(((close-low)-(high-close))/(close-low))','high-delay(high,1)','(open<=delay(open,1)?0:max((high-open),(open-delay(open,1))))','delay(low,1)-low','max(max(high-low,abs(high-delay(close,1))),abs(low-delay(close,1)))']#line:26
condition_list =['tsmax(delta(close,1),4)<0','(rank((avg - close)) / rank((avg + close)))<1','tsmin((open-close)/close,3)<0','(open>=delay(open,1)','max((open-low),(open-delay(open,1))))']#line:32
def random_alpha (OOO0OO0000OOOO000 ,OO000OOO0O0O0O00O ):#line:38
    if OOO0OO0000OOOO000 ==1 :#line:39
        O0O00O000OO0OOO0O =pattern1 ()#line:40
        return O0O00O000OO0OOO0O #line:41
    elif OOO0OO0000OOOO000 ==2 :#line:42
        O0O00O000OO0OOO0O =pattern2 (OO000OOO0O0O0O00O )#line:43
        return O0O00O000OO0OOO0O #line:44
    else :#line:45
        O0O00O000OO0OOO0O =pattern3 ()#line:46
        return O0O00O000OO0OOO0O #line:47
def pattern1 ():#line:50
    O0O00OO0000O00O0O =np .random .choice (len (basic_list ),2 ,replace =False )#line:51
    O000000000O00OO00 =basic_list [O0O00OO0000O00O0O [0 ]]#line:52
    OO0O000OOOOOOO0OO =basic_list [O0O00OO0000O00O0O [1 ]]#line:53
    OO0O0OO00O0OO0OOO =random_oprator ()#line:54
    O000OO00O0O00O00O =random_coeff ()#line:55
    O00OOOOO0OO0OO000 =random_coeff ()#line:56
    if len (OO0O0OO00O0OO0OOO )is not 0 :#line:58
        O0OOOOO00000O00OO ='('+O000OO00O0O00O00O +'*'+O000000000O00OO00 +')'+OO0O0OO00O0OO0OOO +'('+O00OOOOO0OO0OO000 +'*'+OO0O000OOOOOOO0OO +')'#line:59
        return O0OOOOO00000O00OO #line:60
    else :#line:61
        O0OOOOO00000O00OO ='('+O000OO00O0O00O00O +'*'+O000000000O00OO00 +')'#line:62
        return O0OOOOO00000O00OO #line:63
def pattern2 (O0OOOO0OO000OO000 ):#line:66
    O0OOO0OOOOO0O0O0O =pattern1 ()#line:67
    OO00O0OO00O0O0000 =['delta','delay','tsmin','tsmax','std']#line:69
    O0OO0O00O00OOOOOO =OO00O0OO00O0O0000 [np .random .randint (0 ,len (OO00O0OO00O0O0000 ))]#line:70
    OOOOOO00OO00OO00O =str (np .random .randint (1 ,O0OOOO0OO000OO000 ))#line:71
    O0O00O00O00O0O000 =O0OO0O00O00OOOOOO +'('+O0OOO0OOOOO0O0O0O +','+OOOOOO00OO00OO00O +')'#line:73
    return O0O00O00O00O0O000 #line:74
def pattern3 ():#line:77
    O0O00O0O000OO000O =condition_list [np .random .randint (0 ,len (condition_list ))]#line:78
    OOOO00O0OO0O0O0OO =pattern1 ()#line:79
    OO0OOO0O0OOOO000O =pattern1 ()#line:80
    OOOOO00O00OOOOO0O =O0O00O0O000OO000O +'?'+OOOO00O0OO0O0O0OO +':'+OO0OOO0O0OOOO000O #line:82
    return OOOOO00O00OOOOO0O #line:83
def random_oprator ():#line:86
    O0O00000OOO0O0O00 =['+','-','*','/','']#line:87
    OOOOOO000OOOO0OO0 =np .random .choice (5 ,1 ,replace =False ,p =[0.25 ,0.2 ,0.05 ,0.3 ,0.2 ])#line:88
    return O0O00000OOO0O0O00 [OOOOOO000OOOO0OO0 [0 ]]#line:89
def random_coeff ():#line:92
    return str (float (np .random .randint (1 ,20 ))/10 )#line:93
