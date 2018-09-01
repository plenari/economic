#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys #line:3
import globalvar as gl #line:4
import numpy as np #line:5
import pandas as pd #line:6
from sklearn .linear_model import LinearRegression #line:7
init =gl .get_value ('to_init')#line:9
def check_dup (O00O0000OOOO000O0 ):#line:16
    O00OOO0O00O0000O0 =gl .get_value ('listed')#line:17
    return (O00O0000OOOO000O0 in O00OOO0O00O0000O0 [-1 ].columns )#line:18
def close ():#line:22
    return "close()"#line:23
def opened ():#line:26
    return "opened()"#line:27
def high ():#line:30
    return "high()"#line:31
def low ():#line:34
    return "low()"#line:35
def volume ():#line:38
    return "volume()"#line:39
def money ():#line:42
    return "money()"#line:43
def avg ():#line:46
    return "avg()"#line:47
def benchmarkindexopened ():#line:49
    return 'benchmarkindexopened()'#line:50
def benchmarkindexclose ():#line:52
    return 'benchmarkindexclose()'#line:53
def rank (OO00000O0O0OOO000 ):#line:57
    O0O0O0OOOO000O000 ='rank'+'('+OO00000O0O0OOO000 +')'#line:58
    if check_dup (O0O0O0OOOO000O000 ):#line:59
        return O0O0O0OOOO000O000 #line:60
    OOOO0OOOOOOO00OOO =gl .get_value ('listed')#line:61
    if len (OOOO0OOOOOOO00OOO )>=init :#line:62
        O0OOOOO00O0OO0OOO =OOOO0OOOOOOO00OOO [-1 ][OO00000O0O0OOO000 ].rank ()#line:63
        O0O0OOOOO00O0OO00 =O0OOOOO00O0OO0OOO .dropna (axis =0 ,how ='any')#line:64
        OOOO0OOOOOOO00OOO [-1 ][O0O0O0OOOO000O000 ]=(O0OOOOO00O0OO0OOO -1 )/(len (O0O0OOOOO00O0OO00 )-1 )#line:65
    else :#line:66
        OOOO0OOOOOOO00OOO [-1 ][O0O0O0OOOO000O000 ]=list (OOOO0OOOOOOO00OOO [-1 ][OO00000O0O0OOO000 ])#line:67
    gl .set_value ('listed',OOOO0OOOOOOO00OOO )#line:68
    return O0O0O0OOOO000O000 #line:69
def delta (O0O00OO0000OO0O00 ,OO0O0000OOOOO0OO0 ):#line:72
    OO0OO0000OO0OO00O ="delta("+O0O00OO0000OO0O00 +","+str (OO0O0000OOOOO0OO0 )+")"#line:73
    OO0O0000OOOOO0OO0 =int (round (OO0O0000OOOOO0OO0 ))#line:74
    if check_dup (OO0OO0000OO0OO00O ):#line:75
        return OO0OO0000OO0OO00O #line:76
    OOO0OO0OOO00000O0 =gl .get_value ('listed')#line:77
    if len (OOO0OO0OOO00000O0 )<=OO0O0000OOOOO0OO0 :#line:78
        print ('The data is insufficient!')#line:79
        O0000O000000O00O0 =pd .DataFrame (index =OOO0OO0OOO00000O0 [-1 ].index ,columns =[OO0OO0000OO0OO00O ])#line:80
    else :#line:81
        OOOOOOO0O000O000O =OOO0OO0OOO00000O0 [-1 ][O0O00OO0000OO0O00 ]#line:82
        O0O000O00OOO00OO0 =OOO0OO0OOO00000O0 [-(OO0O0000OOOOO0OO0 +1 )][O0O00OO0000OO0O00 ]#line:83
        OOO00000000OO0000 =pd .concat ([OOOOOOO0O000O000O ,O0O000O00OOO00OO0 ],axis =1 ,join ='inner')#line:84
        O0OO00OO0OO00O0OO =np .array (OOO00000000OO0000 )#line:85
        O0000O000000O00O0 =pd .DataFrame (O0OO00OO0OO00O0OO [:,0 ]-O0OO00OO0OO00O0OO [:,1 ],index =OOO00000000OO0000 .index )#line:86
        O0000O000000O00O0 .columns =[OO0OO0000OO0OO00O ]#line:87
    OOO0OO0OOO00000O0 [-1 ]=pd .concat ([OOO0OO0OOO00000O0 [-1 ],O0000O000000O00O0 ],axis =1 ,join ='outer')#line:88
    gl .set_value ('listed',OOO0OO0OOO00000O0 )#line:89
    return OO0OO0000OO0OO00O #line:90
def plus (OO0OO00O0O0000OO0 ,O00OO0OOO000O0O0O ):#line:93
    O00OO0OOOO0OO0O0O ='plus'+'('+str (OO0OO00O0O0000OO0 )+','+str (O00OO0OOO000O0O0O )+')'#line:94
    if check_dup (O00OO0OOOO0OO0O0O ):#line:95
        return O00OO0OOOO0OO0O0O #line:96
    OO00OOOOO00OOOOOO =gl .get_value ('listed')#line:97
    if isinstance (OO0OO00O0O0000OO0 ,str )and isinstance (O00OO0OOO000O0O0O ,str ):#line:98
        OO00OOOOO00OOOOOO [-1 ][O00OO0OOOO0OO0O0O ]=OO00OOOOO00OOOOOO [-1 ][OO0OO00O0O0000OO0 ]+OO00OOOOO00OOOOOO [-1 ][O00OO0OOO000O0O0O ]#line:99
    elif isinstance (OO0OO00O0O0000OO0 ,str ):#line:100
        OO00OOOOO00OOOOOO [-1 ][O00OO0OOOO0OO0O0O ]=OO00OOOOO00OOOOOO [-1 ][OO0OO00O0O0000OO0 ]+O00OO0OOO000O0O0O #line:101
    elif isinstance (O00OO0OOO000O0O0O ,str ):#line:102
        OO00OOOOO00OOOOOO [-1 ][O00OO0OOOO0OO0O0O ]=OO00OOOOO00OOOOOO [-1 ][O00OO0OOO000O0O0O ]+OO0OO00O0O0000OO0 #line:103
    elif not isinstance (OO0OO00O0O0000OO0 ,str )and not isinstance (O00OO0OOO000O0O0O ,str ):#line:104
        OO00OOOOO00OOOOOO [-1 ][O00OO0OOOO0OO0O0O ]=OO0OO00O0O0000OO0 +O00OO0OOO000O0O0O #line:105
    gl .set_value ('listed',OO00OOOOO00OOOOOO )#line:106
    return O00OO0OOOO0OO0O0O #line:107
def subtract (OO0OOOOOO0OOOOO0O ,OOO0O00OOOO0O0O0O ):#line:110
    O0OOO0OO00OO000O0 ='subtract'+'('+str (OO0OOOOOO0OOOOO0O )+','+str (OOO0O00OOOO0O0O0O )+')'#line:111
    if check_dup (O0OOO0OO00OO000O0 ):#line:112
        return O0OOO0OO00OO000O0 #line:113
    O000O0OOOOO0OOO00 =gl .get_value ('listed')#line:114
    if isinstance (OO0OOOOOO0OOOOO0O ,str )and isinstance (OOO0O00OOOO0O0O0O ,str ):#line:115
        O000O0OOOOO0OOO00 [-1 ][O0OOO0OO00OO000O0 ]=O000O0OOOOO0OOO00 [-1 ][OO0OOOOOO0OOOOO0O ]-O000O0OOOOO0OOO00 [-1 ][OOO0O00OOOO0O0O0O ]#line:116
    elif isinstance (OO0OOOOOO0OOOOO0O ,str ):#line:117
        O000O0OOOOO0OOO00 [-1 ][O0OOO0OO00OO000O0 ]=O000O0OOOOO0OOO00 [-1 ][OO0OOOOOO0OOOOO0O ]-OOO0O00OOOO0O0O0O #line:118
    elif isinstance (OOO0O00OOOO0O0O0O ,str ):#line:119
        O000O0OOOOO0OOO00 [-1 ][O0OOO0OO00OO000O0 ]=OO0OOOOOO0OOOOO0O -O000O0OOOOO0OOO00 [-1 ][OOO0O00OOOO0O0O0O ]#line:120
    elif not isinstance (OO0OOOOOO0OOOOO0O ,str )and not isinstance (OOO0O00OOOO0O0O0O ,str ):#line:121
        O000O0OOOOO0OOO00 [-1 ][O0OOO0OO00OO000O0 ]=OO0OOOOOO0OOOOO0O -OOO0O00OOOO0O0O0O #line:122
    gl .set_value ('listed',O000O0OOOOO0OOO00 )#line:123
    return O0OOO0OO00OO000O0 #line:124
def multiply (OO00OO0OO00O0OOOO ,OO000OOO00OO0O0OO ):#line:127
    OOO0O0O0O00OOOO0O ='multiply'+'('+str (OO00OO0OO00O0OOOO )+','+str (OO000OOO00OO0O0OO )+')'#line:128
    if check_dup (OOO0O0O0O00OOOO0O ):#line:129
        return OOO0O0O0O00OOOO0O #line:130
    OO0OO0OOO000O0000 =gl .get_value ('listed')#line:131
    if isinstance (OO00OO0OO00O0OOOO ,str )and isinstance (OO000OOO00OO0O0OO ,str ):#line:132
        OO0OO0OOO000O0000 [-1 ][OOO0O0O0O00OOOO0O ]=OO0OO0OOO000O0000 [-1 ][OO00OO0OO00O0OOOO ]*OO0OO0OOO000O0000 [-1 ][OO000OOO00OO0O0OO ]#line:133
    elif isinstance (OO00OO0OO00O0OOOO ,str ):#line:134
        OO0OO0OOO000O0000 [-1 ][OOO0O0O0O00OOOO0O ]=OO0OO0OOO000O0000 [-1 ][OO00OO0OO00O0OOOO ]*OO000OOO00OO0O0OO #line:135
    elif isinstance (OO000OOO00OO0O0OO ,str ):#line:136
        OO0OO0OOO000O0000 [-1 ][OOO0O0O0O00OOOO0O ]=OO0OO0OOO000O0000 [-1 ][OO000OOO00OO0O0OO ]*OO00OO0OO00O0OOOO #line:137
    elif not isinstance (OO00OO0OO00O0OOOO ,str )and not isinstance (OO000OOO00OO0O0OO ,str ):#line:138
        OO0OO0OOO000O0000 [-1 ][OOO0O0O0O00OOOO0O ]=OO00OO0OO00O0OOOO *OO000OOO00OO0O0OO #line:139
    gl .set_value ('listed',OO0OO0OOO000O0000 )#line:140
    return OOO0O0O0O00OOOO0O #line:141
def divide (OOOOOOO00OO00OOO0 ,O00O0OO00O0O00O00 ):#line:144
    OOOO000000O0O00O0 ='divide'+'('+str (OOOOOOO00OO00OOO0 )+','+str (O00O0OO00O0O00O00 )+')'#line:145
    if check_dup (OOOO000000O0O00O0 ):#line:146
        return OOOO000000O0O00O0 #line:147
    OOOO0O0OO0000000O =gl .get_value ('listed')#line:148
    if isinstance (OOOOOOO00OO00OOO0 ,str )and isinstance (O00O0OO00O0O00O00 ,str ):#line:149
        OOOO0O0OO0000000O [-1 ][O00O0OO00O0O00O00 ][OOOO0O0OO0000000O [-1 ][O00O0OO00O0O00O00 ]==0 ]=np .nan #line:150
        OOOO0O0OO0000000O [-1 ][OOOO000000O0O00O0 ]=OOOO0O0OO0000000O [-1 ][OOOOOOO00OO00OOO0 ]/OOOO0O0OO0000000O [-1 ][O00O0OO00O0O00O00 ]#line:151
    elif isinstance (OOOOOOO00OO00OOO0 ,str ):#line:152
        if O00O0OO00O0O00O00 !=0 :#line:153
            OOO0000OO000O0000 =O00O0OO00O0O00O00 #line:154
        else :#line:155
            OOO0000OO000O0000 =np .nan #line:156
        OOOO0O0OO0000000O [-1 ][OOOO000000O0O00O0 ]=OOOO0O0OO0000000O [-1 ][OOOOOOO00OO00OOO0 ]/OOO0000OO000O0000 #line:157
    elif isinstance (O00O0OO00O0O00O00 ,str ):#line:158
        OOOO0O0OO0000000O [-1 ][O00O0OO00O0O00O00 ][OOOO0O0OO0000000O [-1 ][O00O0OO00O0O00O00 ]==0 ]=np .nan #line:159
        OOOO0O0OO0000000O [-1 ][OOOO000000O0O00O0 ]=OOOOOOO00OO00OOO0 /OOOO0O0OO0000000O [-1 ][O00O0OO00O0O00O00 ]#line:160
    elif not isinstance (OOOOOOO00OO00OOO0 ,str )and not isinstance (O00O0OO00O0O00O00 ,str ):#line:161
        if O00O0OO00O0O00O00 !=0 :#line:162
            OOO0000OO000O0000 =O00O0OO00O0O00O00 #line:163
        else :#line:164
            OOO0000OO000O0000 =np .nan #line:165
        OOOO0O0OO0000000O [-1 ][OOOO000000O0O00O0 ]=OOOOOOO00OO00OOO0 /OOO0000OO000O0000 #line:166
    gl .set_value ('listed',OOOO0O0OO0000000O )#line:167
    return OOOO000000O0O00O0 #line:168
def power (O00OO0OOOO0OO000O ,OO00OOO0O0O0O000O ):#line:170
    OOOOO0000O0OOO0O0 ='power'+'('+str (O00OO0OOOO0OO000O )+','+str (OO00OOO0O0O0O000O )+')'#line:171
    if check_dup (OOOOO0000O0OOO0O0 ):#line:172
        return OOOOO0000O0OOO0O0 #line:173
    O00OOO00O0OOOO0O0 =gl .get_value ('listed')#line:174
    if isinstance (O00OO0OOOO0OO000O ,str )and isinstance (OO00OOO0O0O0O000O ,str ):#line:175
        O00OOO00O0OOOO0O0 [-1 ][OOOOO0000O0OOO0O0 ]=O00OOO00O0OOOO0O0 [-1 ][O00OO0OOOO0OO000O ]**O00OOO00O0OOOO0O0 [-1 ][OO00OOO0O0O0O000O ]#line:176
    elif isinstance (O00OO0OOOO0OO000O ,str ):#line:177
        O00OOO00O0OOOO0O0 [-1 ][OOOOO0000O0OOO0O0 ]=O00OOO00O0OOOO0O0 [-1 ][O00OO0OOOO0OO000O ]**OO00OOO0O0O0O000O #line:178
    elif isinstance (OO00OOO0O0O0O000O ,str ):#line:179
        O00OOO00O0OOOO0O0 [-1 ][OOOOO0000O0OOO0O0 ]=O00OO0OOOO0OO000O **O00OOO00O0OOOO0O0 [-1 ][OO00OOO0O0O0O000O ]#line:180
    elif not isinstance (O00OO0OOOO0OO000O ,str )and not isinstance (OO00OOO0O0O0O000O ,str ):#line:181
        O00OOO00O0OOOO0O0 [-1 ][OOOOO0000O0OOO0O0 ]=O00OO0OOOO0OO000O **OO00OOO0O0O0O000O #line:182
    gl .set_value ('listed',O00OOO00O0OOOO0O0 )#line:183
    return OOOOO0000O0OOO0O0 #line:184
def signedpower (O0O000OOO0000O0OO ,OO0OOO0OO0OO0OO00 ):#line:189
    O0OO000O0OOOO00OO ='signedpower'+'('+str (O0O000OOO0000O0OO )+','+str (OO0OOO0OO0OO0OO00 )+')'#line:190
    if check_dup (O0OO000O0OOOO00OO ):#line:191
        return O0OO000O0OOOO00OO #line:192
    O000O00O0OOOO0OO0 =gl .get_value ('listed')#line:193
    if isinstance (O0O000OOO0000O0OO ,str )and isinstance (OO0OOO0OO0OO0OO00 ,str ):#line:194
        O000O00O0OOOO0OO0 [-1 ][O0OO000O0OOOO00OO ]=np .sign (O000O00O0OOOO0OO0 [-1 ][O0O000OOO0000O0OO ])*(abs (O000O00O0OOOO0OO0 [-1 ][O0O000OOO0000O0OO ])**O000O00O0OOOO0OO0 [-1 ][OO0OOO0OO0OO0OO00 ])#line:195
    elif isinstance (O0O000OOO0000O0OO ,str ):#line:196
        O000O00O0OOOO0OO0 [-1 ][O0OO000O0OOOO00OO ]=np .sign (O000O00O0OOOO0OO0 [-1 ][O0O000OOO0000O0OO ])*(abs (O000O00O0OOOO0OO0 [-1 ][O0O000OOO0000O0OO ])**OO0OOO0OO0OO0OO00 )#line:197
    elif isinstance (OO0OOO0OO0OO0OO00 ,str ):#line:198
        O000O00O0OOOO0OO0 [-1 ][O0OO000O0OOOO00OO ]=np .sign (O0O000OOO0000O0OO )*(abs (O0O000OOO0000O0OO )**O000O00O0OOOO0OO0 [-1 ][OO0OOO0OO0OO0OO00 ])#line:199
    elif not isinstance (O0O000OOO0000O0OO ,str )and not isinstance (OO0OOO0OO0OO0OO00 ,str ):#line:200
        O000O00O0OOOO0OO0 [-1 ][O0OO000O0OOOO00OO ]=np .sign (O0O000OOO0000O0OO )*(abs (O0O000OOO0000O0OO )**OO0OOO0OO0OO0OO00 )#line:201
    gl .set_value ('listed',O000O00O0OOOO0OO0 )#line:202
    return O0OO000O0OOOO00OO #line:203
def delay (OO0OO00OO0O0OO0O0 ,O0OO0O0OO00O0OO00 ):#line:206
    OOOOOOO0000O00O0O ="delay("+OO0OO00OO0O0OO0O0 +","+str (O0OO0O0OO00O0OO00 )+")"#line:207
    O0OO0O0OO00O0OO00 =int (round (O0OO0O0OO00O0OO00 ))#line:208
    if check_dup (OOOOOOO0000O00O0O ):#line:209
        return OOOOOOO0000O00O0O #line:210
    O0OO00O0O00O0O0O0 =gl .get_value ('listed')#line:211
    if len (O0OO00O0O00O0O0O0 )<=O0OO0O0OO00O0OO00 :#line:212
        print ('The data is insufficient!')#line:213
        O0O0OOOO000O00O00 =pd .DataFrame (index =O0OO00O0O00O0O0O0 [-1 ].index ,columns =[OOOOOOO0000O00O0O ])#line:214
    else :#line:215
        O0OOOOO0000OO0OOO =O0OO00O0O00O0O0O0 [-(O0OO0O0OO00O0OO00 +1 )][OO0OO00OO0O0OO0O0 ]#line:216
        O0O0OOOO000O00O00 =pd .DataFrame (O0OO00O0O00O0O0O0 [-(O0OO0O0OO00O0OO00 +1 )][OO0OO00OO0O0OO0O0 ])#line:217
        O0O0OOOO000O00O00 .columns =[OOOOOOO0000O00O0O ]#line:218
    O0OO00O0O00O0O0O0 [-1 ]=pd .concat ([O0OO00O0O00O0O0O0 [-1 ],O0O0OOOO000O00O00 ],axis =1 ,join ='outer')#line:219
    gl .set_value ('listed',O0OO00O0O00O0O0O0 )#line:220
    return OOOOOOO0000O00O0O #line:221
def corr (O0OO0O0OO0OOOOOOO ,OOOO0000O0O0OOO0O ,OOOO000O0O000OOOO ):#line:224
    O0000OOOO0OOOOO0O ="corr("+O0OO0O0OO0OOOOOOO +","+OOOO0000O0O0OOO0O +","+str (OOOO000O0O000OOOO )+")"#line:225
    OOOO000O0O000OOOO =int (round (OOOO000O0O000OOOO ))#line:226
    if check_dup (O0000OOOO0OOOOO0O ):#line:227
        return O0000OOOO0OOOOO0O #line:228
    OOO0O00000OO000OO =gl .get_value ('listed')#line:229
    if len (OOO0O00000OO000OO )<=OOOO000O0O000OOOO :#line:230
        print ('The data is insufficient!')#line:231
        OOOO00OO00O0OOOOO =pd .DataFrame (index =OOO0O00000OO000OO [-1 ].index ,columns =[O0000OOOO0OOOOO0O ])#line:232
    else :#line:233
        O0OO00OO0O00O0O00 =pd .DataFrame (index =OOO0O00000OO000OO [-1 ].index )#line:234
        OO00OOOOO0O00OO0O =pd .DataFrame (index =OOO0O00000OO000OO [-1 ].index )#line:235
        for OO0OOOO00O0OOOO00 in range (1 ,OOOO000O0O000OOOO +1 ):#line:236
            OOOOO0OO0000OO0O0 =pd .DataFrame (OOO0O00000OO000OO [(-OO0OOOO00O0OOOO00 )][[O0OO0O0OO0OOOOOOO ,OOOO0000O0O0OOO0O ]])#line:237
            OOOOO0OO0000OO0O0 .columns =[['ca'+str (OO0OOOO00O0OOOO00 ),'cb'+str (OO0OOOO00O0OOOO00 )]]#line:238
            OOOOO0OO0000OO0O0 =OOOOO0OO0000OO0O0 .dropna (axis =0 ,how ='any')#line:239
            O0OO00OO0O00O0O00 =pd .concat ([O0OO00OO0O00O0O00 ,OOOOO0OO0000OO0O0 ['ca'+str (OO0OOOO00O0OOOO00 )]],axis =1 ,join ='inner')#line:240
            OO00OOOOO0O00OO0O =pd .concat ([OO00OOOOO0O00OO0O ,OOOOO0OO0000OO0O0 ['cb'+str (OO0OOOO00O0OOOO00 )]],axis =1 ,join ='inner')#line:241
        O00OOOO00OOOOO00O =np .array (O0OO00OO0O00O0O00 )#line:242
        OOO0OO0000O000000 =np .array (OO00OOOOO0O00OO0O )#line:243
        OOOO00OO00O0OOOOO =[]#line:244
        for OO0OOOO00O0OOOO00 in range (len (O0OO00OO0O00O0O00 )):#line:245
            OOOO00OO00O0OOOOO .append (np .corrcoef (O00OOOO00OOOOO00O [OO0OOOO00O0OOOO00 ,:],OOO0OO0000O000000 [OO0OOOO00O0OOOO00 ,:])[0 ,1 ])#line:246
        OOOO00OO00O0OOOOO =pd .DataFrame (OOOO00OO00O0OOOOO ,index =O0OO00OO0O00O0O00 .index ,columns =[O0000OOOO0OOOOO0O ])#line:247
    OOO0O00000OO000OO [-1 ]=pd .concat ([OOO0O00000OO000OO [-1 ],OOOO00OO00O0OOOOO ],axis =1 ,join ='outer')#line:248
    gl .set_value ('listed',OOO0O00000OO000OO )#line:249
    return O0000OOOO0OOOOO0O #line:250
def cov (OOO0000OO0OO0OO0O ,O00OOO00O0O0OOOOO ,O0OOOO00OOOO0OOO0 ):#line:253
    OOOO0O0OO0O00O0O0 ="cov("+OOO0000OO0OO0OO0O +","+O00OOO00O0O0OOOOO +","+str (O0OOOO00OOOO0OOO0 )+")"#line:254
    O0OOOO00OOOO0OOO0 =int (round (O0OOOO00OOOO0OOO0 ))#line:255
    if check_dup (OOOO0O0OO0O00O0O0 ):#line:256
        return OOOO0O0OO0O00O0O0 #line:257
    O0O00000O0000OO00 =gl .get_value ('listed')#line:258
    if len (O0O00000O0000OO00 )<=O0OOOO00OOOO0OOO0 :#line:259
        print ('The data is insufficient!')#line:260
        OOO00O0OO0OO0O000 =pd .DataFrame (index =O0O00000O0000OO00 [-1 ].index ,columns =[OOOO0O0OO0O00O0O0 ])#line:261
    else :#line:262
        O0O0O000O0O0OO00O =pd .DataFrame (index =O0O00000O0000OO00 [-1 ].index )#line:263
        OOOO0O0O00O0O0O00 =pd .DataFrame (index =O0O00000O0000OO00 [-1 ].index )#line:264
        for O0000OO00OOOO0OOO in range (1 ,O0OOOO00OOOO0OOO0 +1 ):#line:265
            OO0O00000OO0000OO =pd .DataFrame (O0O00000O0000OO00 [(-O0000OO00OOOO0OOO )][OOO0000OO0OO0OO0O ])#line:266
            OO0O00000OO0000OO .columns =['ca'+str (O0000OO00OOOO0OOO )]#line:267
            O0000OO000OO0O0OO =pd .DataFrame (O0O00000O0000OO00 [(-O0000OO00OOOO0OOO )][O00OOO00O0O0OOOOO ])#line:268
            O0000OO000OO0O0OO .columns =['cb'+str (O0000OO00OOOO0OOO )]#line:269
            O0O0O000O0O0OO00O =pd .concat ([O0O0O000O0O0OO00O ,OO0O00000OO0000OO ],axis =1 ,join ='inner')#line:270
            OOOO0O0O00O0O0O00 =pd .concat ([OOOO0O0O00O0O0O00 ,O0000OO000OO0O0OO ],axis =1 ,join ='inner')#line:271
        OOO0OOO0OOOOO0O00 =np .array (O0O0O000O0O0OO00O )#line:272
        O000OO0OOOO0O0OO0 =np .array (OOOO0O0O00O0O0O00 )#line:273
        OOO00O0OO0OO0O000 =[]#line:274
        for O0000OO00OOOO0OOO in range (len (O0O0O000O0O0OO00O )):#line:275
            OOO00O0OO0OO0O000 .append (np .cov (OOO0OOO0OOOOO0O00 [O0000OO00OOOO0OOO ,:],O000OO0OOOO0O0OO0 [O0000OO00OOOO0OOO ,:])[0 ,1 ])#line:276
        OOO00O0OO0OO0O000 =pd .DataFrame (OOO00O0OO0OO0O000 ,index =O0O0O000O0O0OO00O .index ,columns =[OOOO0O0OO0O00O0O0 ])#line:277
    O0O00000O0000OO00 [-1 ]=pd .concat ([O0O00000O0000OO00 [-1 ],OOO00O0OO0OO0O000 ],axis =1 ,join ='outer')#line:278
    gl .set_value ('listed',O0O00000O0000OO00 )#line:279
    return OOOO0O0OO0O00O0O0 #line:280
def exponential (O0OO00OOO00000O0O ):#line:283
    OOO0O0000O0OOOOOO ='exponential'+'('+str (O0OO00OOO00000O0O )+')'#line:284
    if check_dup (OOO0O0000O0OOOOOO ):#line:285
        return OOO0O0000O0OOOOOO #line:286
    OO0O0000OO00000O0 =gl .get_value ('listed')#line:287
    if isinstance (O0OO00OOO00000O0O ,str ):#line:288
        OO0O0000OO00000O0 [-1 ][OOO0O0000O0OOOOOO ]=np .exp (OO0O0000OO00000O0 [-1 ][O0OO00OOO00000O0O ])#line:289
    else :#line:290
        OO0O0000OO00000O0 [-1 ][OOO0O0000O0OOOOOO ]=np .exp (O0OO00OOO00000O0O )#line:291
    gl .set_value ('listed',OO0O0000OO00000O0 )#line:292
    return OOO0O0000O0OOOOOO #line:293
def logarithm (OOOO0OO0O0OO00OOO ):#line:296
    O00OO00OOOO0OO0O0 ='logarithm'+'('+str (OOOO0OO0O0OO00OOO )+')'#line:297
    if check_dup (O00OO00OOOO0OO0O0 ):#line:298
        return O00OO00OOOO0OO0O0 #line:299
    O00O0OO0000OOO00O =gl .get_value ('listed')#line:300
    if isinstance (OOOO0OO0O0OO00OOO ,str ):#line:301
        O00O0OO0000OOO00O [-1 ][O00OO00OOOO0OO0O0 ]=np .log (O00O0OO0000OOO00O [-1 ][OOOO0OO0O0OO00OOO ],dtype =float )#line:302
    else :#line:303
        O00O0OO0000OOO00O [-1 ][O00OO00OOOO0OO0O0 ]=np .log (OOOO0OO0O0OO00OOO )#line:304
    gl .set_value ('listed',O00O0OO0000OOO00O )#line:305
    return O00OO00OOOO0OO0O0 #line:306
def sign (OO000O00OOOOOOOOO ):#line:309
    OOOOO00O0O0OO000O ='sign'+'('+str (OO000O00OOOOOOOOO )+')'#line:310
    if check_dup (OOOOO00O0O0OO000O ):#line:311
        return OOOOO00O0O0OO000O #line:312
    O0OO0O0O0OO000000 =gl .get_value ('listed')#line:313
    if isinstance (OO000O00OOOOOOOOO ,str ):#line:314
        O0OO0O0O0OO000000 [-1 ][OOOOO00O0O0OO000O ]=np .sign (O0OO0O0O0OO000000 [-1 ][OO000O00OOOOOOOOO ])#line:315
    else :#line:316
        O0OO0O0O0OO000000 [-1 ][OOOOO00O0O0OO000O ]=np .sign (OO000O00OOOOOOOOO )#line:317
    gl .set_value ('listed',O0OO0O0O0OO000000 )#line:318
    return OOOOO00O0O0OO000O #line:319
def arccos (OO00OO00OO0OO0OOO ):#line:322
    OOOOOOOO0OO000000 ='arccos'+'('+str (OO00OO00OO0OO0OOO )+')'#line:323
    if check_dup (OOOOOOOO0OO000000 ):#line:324
        return OOOOOOOO0OO000000 #line:325
    O0O00000OO0O0O00O =gl .get_value ('listed')#line:326
    if isinstance (OO00OO00OO0OO0OOO ,str ):#line:327
        O0O00000OO0O0O00O [-1 ][OOOOOOOO0OO000000 ]=np .arccos (O0O00000OO0O0O00O [-1 ][OO00OO00OO0OO0OOO ])#line:328
    else :#line:329
        O0O00000OO0O0O00O [-1 ][OOOOOOOO0OO000000 ]=np .arccos (OO00OO00OO0OO0OOO )#line:330
    gl .set_value ('listed',O0O00000OO0O0O00O )#line:331
    return OOOOOOOO0OO000000 #line:332
def arcsin (O0O0000000O0OOO0O ):#line:335
    O0OOOOO0O00OOOO0O ='arcsin'+'('+str (O0O0000000O0OOO0O )+')'#line:336
    if check_dup (O0OOOOO0O00OOOO0O ):#line:337
        return O0OOOOO0O00OOOO0O #line:338
    O000O0OOOOOOOO00O =gl .get_value ('listed')#line:339
    if isinstance (O0O0000000O0OOO0O ,str ):#line:340
        O000O0OOOOOOOO00O [-1 ][O0OOOOO0O00OOOO0O ]=np .arcsin (O000O0OOOOOOOO00O [-1 ][O0O0000000O0OOO0O ])#line:341
    else :#line:342
        O000O0OOOOOOOO00O [-1 ][O0OOOOO0O00OOOO0O ]=np .arcsin (O0O0000000O0OOO0O )#line:343
    gl .set_value ('listed',O000O0OOOOOOOO00O )#line:344
    return O0OOOOO0O00OOOO0O #line:345
def arctan (O0OO0O000OOOOO0OO ):#line:348
    OOOOO000O00000000 ='arctan'+'('+str (O0OO0O000OOOOO0OO )+')'#line:349
    if check_dup (OOOOO000O00000000 ):#line:350
        return OOOOO000O00000000 #line:351
    O0OO0OO0O000000OO =gl .get_value ('listed')#line:352
    if isinstance (O0OO0O000OOOOO0OO ,str ):#line:353
        O0OO0OO0O000000OO [-1 ][OOOOO000O00000000 ]=np .arctan (O0OO0OO0O000000OO [-1 ][O0OO0O000OOOOO0OO ])#line:354
    else :#line:355
        O0OO0OO0O000000OO [-1 ][OOOOO000O00000000 ]=np .arctan (O0OO0O000OOOOO0OO )#line:356
    gl .set_value ('listed',O0OO0OO0O000000OO )#line:357
    return OOOOO000O00000000 #line:358
def arccosh (O0O000O000OO00OOO ):#line:361
    OO0O0OOOO00OO00O0 ='arccosh'+'('+str (O0O000O000OO00OOO )+')'#line:362
    if check_dup (OO0O0OOOO00OO00O0 ):#line:363
        return OO0O0OOOO00OO00O0 #line:364
    O00O000000000O000 =gl .get_value ('listed')#line:365
    if isinstance (O0O000O000OO00OOO ,str ):#line:366
        O00O000000000O000 [-1 ][OO0O0OOOO00OO00O0 ]=np .arccosh (O00O000000000O000 [-1 ][O0O000O000OO00OOO ])#line:367
    else :#line:368
        O00O000000000O000 [-1 ][OO0O0OOOO00OO00O0 ]=np .arccosh (O0O000O000OO00OOO )#line:369
    gl .set_value ('listed',O00O000000000O000 )#line:370
    return OO0O0OOOO00OO00O0 #line:371
def arcsinh (OO0OO000O00O0O00O ):#line:374
    O0OO0O00OOO00OO0O ='arcsinh'+'('+str (OO0OO000O00O0O00O )+')'#line:375
    if check_dup (O0OO0O00OOO00OO0O ):#line:376
        return O0OO0O00OOO00OO0O #line:377
    OO00O0OOOOO00O0O0 =gl .get_value ('listed')#line:378
    if isinstance (OO0OO000O00O0O00O ,str ):#line:379
        OO00O0OOOOO00O0O0 [-1 ][O0OO0O00OOO00OO0O ]=np .arcsinh (OO00O0OOOOO00O0O0 [-1 ][OO0OO000O00O0O00O ])#line:380
    else :#line:381
        OO00O0OOOOO00O0O0 [-1 ][O0OO0O00OOO00OO0O ]=np .arcsinh (OO0OO000O00O0O00O )#line:382
    gl .set_value ('listed',OO00O0OOOOO00O0O0 )#line:383
    return O0OO0O00OOO00OO0O #line:384
def arctanh (O00000OOO0OOOOO0O ):#line:387
    O0O0OO0OOO00O0OOO ='arctanh'+'('+str (O00000OOO0OOOOO0O )+')'#line:388
    if check_dup (O0O0OO0OOO00O0OOO ):#line:389
        return O0O0OO0OOO00O0OOO #line:390
    OO0OO0OOO000OO0OO =gl .get_value ('listed')#line:391
    if isinstance (O00000OOO0OOOOO0O ,str ):#line:392
        OO0OO0OOO000OO0OO [-1 ][O0O0OO0OOO00O0OOO ]=np .arctanh (OO0OO0OOO000OO0OO [-1 ][O00000OOO0OOOOO0O ])#line:393
    else :#line:394
        OO0OO0OOO000OO0OO [-1 ][O0O0OO0OOO00O0OOO ]=np .arctanh (O00000OOO0OOOOO0O )#line:395
    gl .set_value ('listed',OO0OO0OOO000OO0OO )#line:396
    return O0O0OO0OOO00O0OOO #line:397
def cos (O00OO0000OO0O00O0 ):#line:400
    O0O00000OOOOO00OO ='cos'+'('+str (O00OO0000OO0O00O0 )+')'#line:401
    if check_dup (O0O00000OOOOO00OO ):#line:402
        return O0O00000OOOOO00OO #line:403
    O0OO000O0O0OOOOO0 =gl .get_value ('listed')#line:404
    if isinstance (O00OO0000OO0O00O0 ,str ):#line:405
        O0OO000O0O0OOOOO0 [-1 ][O0O00000OOOOO00OO ]=np .cos (O0OO000O0O0OOOOO0 [-1 ][O00OO0000OO0O00O0 ])#line:406
    else :#line:407
        O0OO000O0O0OOOOO0 [-1 ][O0O00000OOOOO00OO ]=np .cos (O00OO0000OO0O00O0 )#line:408
    gl .set_value ('listed',O0OO000O0O0OOOOO0 )#line:409
    return O0O00000OOOOO00OO #line:410
def sin (O00O0OOOOOOO00O00 ):#line:413
    O000O0O00OOO00O0O ='sin'+'('+str (O00O0OOOOOOO00O00 )+')'#line:414
    if check_dup (O000O0O00OOO00O0O ):#line:415
        return O000O0O00OOO00O0O #line:416
    O0000000O0O00000O =gl .get_value ('listed')#line:417
    if isinstance (O00O0OOOOOOO00O00 ,str ):#line:418
        O0000000O0O00000O [-1 ][O000O0O00OOO00O0O ]=np .sin (O0000000O0O00000O [-1 ][O00O0OOOOOOO00O00 ])#line:419
    else :#line:420
        O0000000O0O00000O [-1 ][O000O0O00OOO00O0O ]=np .sin (O00O0OOOOOOO00O00 )#line:421
    gl .set_value ('listed',O0000000O0O00000O )#line:422
    return O000O0O00OOO00O0O #line:423
def tan (O00000OOO0OO00O0O ):#line:426
    O000O0O0O0000O0O0 ='tan'+'('+str (O00000OOO0OO00O0O )+')'#line:427
    if check_dup (O000O0O0O0000O0O0 ):#line:428
        return O000O0O0O0000O0O0 #line:429
    OO0000O00OOOO0O0O =gl .get_value ('listed')#line:430
    if isinstance (O00000OOO0OO00O0O ,str ):#line:431
        OO0000O00OOOO0O0O [-1 ][O000O0O0O0000O0O0 ]=np .tan (OO0000O00OOOO0O0O [-1 ][O00000OOO0OO00O0O ])#line:432
    else :#line:433
        OO0000O00OOOO0O0O [-1 ][O000O0O0O0000O0O0 ]=np .tan (O00000OOO0OO00O0O )#line:434
    gl .set_value ('listed',OO0000O00OOOO0O0O )#line:435
    return O000O0O0O0000O0O0 #line:436
def cosh (OO0O0OOOOO00000O0 ):#line:439
    O0O0OO00OOO00O0OO ='cosh'+'('+str (OO0O0OOOOO00000O0 )+')'#line:440
    if check_dup (O0O0OO00OOO00O0OO ):#line:441
        return O0O0OO00OOO00O0OO #line:442
    OOO00000OO0O000OO =gl .get_value ('listed')#line:443
    if isinstance (OO0O0OOOOO00000O0 ,str ):#line:444
        OOO00000OO0O000OO [-1 ][O0O0OO00OOO00O0OO ]=np .cosh (OOO00000OO0O000OO [-1 ][OO0O0OOOOO00000O0 ])#line:445
    else :#line:446
        OOO00000OO0O000OO [-1 ][O0O0OO00OOO00O0OO ]=np .cosh (OO0O0OOOOO00000O0 )#line:447
    gl .set_value ('listed',OOO00000OO0O000OO )#line:448
    return O0O0OO00OOO00O0OO #line:449
def sinh (OOO000000OOO000OO ):#line:452
    OO0OOOOOO0OO0O00O ='sinh'+'('+str (OOO000000OOO000OO )+')'#line:453
    if check_dup (OO0OOOOOO0OO0O00O ):#line:454
        return OO0OOOOOO0OO0O00O #line:455
    O0O0000000OOOO000 =gl .get_value ('listed')#line:456
    if isinstance (OOO000000OOO000OO ,str ):#line:457
        O0O0000000OOOO000 [-1 ][OO0OOOOOO0OO0O00O ]=np .sinh (O0O0000000OOOO000 [-1 ][OOO000000OOO000OO ])#line:458
    else :#line:459
        O0O0000000OOOO000 [-1 ][OO0OOOOOO0OO0O00O ]=np .sinh (OOO000000OOO000OO )#line:460
    gl .set_value ('listed',O0O0000000OOOO000 )#line:461
    return OO0OOOOOO0OO0O00O #line:462
def tanh (OOOOOOO000000OOOO ):#line:465
    O000000O0O0000O00 ='tanh'+'('+str (OOOOOOO000000OOOO )+')'#line:466
    if check_dup (O000000O0O0000O00 ):#line:467
        return O000000O0O0000O00 #line:468
    OOO00OO0OO0O0O00O =gl .get_value ('listed')#line:469
    if isinstance (OOOOOOO000000OOOO ,str ):#line:470
        OOO00OO0OO0O0O00O [-1 ][O000000O0O0000O00 ]=np .tanh (OOO00OO0OO0O0O00O [-1 ][OOOOOOO000000OOOO ])#line:471
    else :#line:472
        OOO00OO0OO0O0O00O [-1 ][O000000O0O0000O00 ]=np .tanh (OOOOOOO000000OOOO )#line:473
    gl .set_value ('listed',OOO00OO0OO0O0O00O )#line:474
    return O000000O0O0000O00 #line:475
def absolute (O000O000OO0O0OOOO ):#line:478
    OO0OO00O0OOO0O000 ='absolute'+'('+str (O000O000OO0O0OOOO )+')'#line:479
    if check_dup (OO0OO00O0OOO0O000 ):#line:480
        return OO0OO00O0OOO0O000 #line:481
    O0OO00O0OOOOO0OO0 =gl .get_value ('listed')#line:482
    if isinstance (O000O000OO0O0OOOO ,str ):#line:483
        O0OO00O0OOOOO0OO0 [-1 ][OO0OO00O0OOO0O000 ]=np .abs (O0OO00O0OOOOO0OO0 [-1 ][O000O000OO0O0OOOO ])#line:484
    else :#line:485
        O0OO00O0OOOOO0OO0 [-1 ][OO0OO00O0OOO0O000 ]=np .abs (O000O000OO0O0OOOO )#line:486
    gl .set_value ('listed',O0OO00O0OOOOO0OO0 )#line:487
    return OO0OO00O0OOO0O000 #line:488
def ceiling (O00000OO000000OO0 ):#line:491
    O0O0OO0OO0O0O00O0 ='ceiling'+'('+str (O00000OO000000OO0 )+')'#line:493
    if check_dup (O0O0OO0OO0O0O00O0 ):#line:494
        return O0O0OO0OO0O0O00O0 #line:495
    O000000OO0O000O00 =gl .get_value ('listed')#line:496
    if isinstance (O00000OO000000OO0 ,str ):#line:497
        O000000OO0O000O00 [-1 ][O0O0OO0OO0O0O00O0 ]=np .ceil (O000000OO0O000O00 [-1 ][O00000OO000000OO0 ])#line:498
    else :#line:499
        O000000OO0O000O00 [-1 ][O0O0OO0OO0O0O00O0 ]=np .ceil (O00000OO000000OO0 )#line:500
    gl .set_value ('listed',O000000OO0O000O00 )#line:501
    return O0O0OO0OO0O0O00O0 #line:502
def floor (O00OO0000O000OO0O ):#line:505
    O0OO0O0OOO0O0OO0O ='floor'+'('+str (O00OO0000O000OO0O )+')'#line:507
    if check_dup (O0OO0O0OOO0O0OO0O ):#line:508
        return O0OO0O0OOO0O0OO0O #line:509
    O00OO00000OOO0OOO =gl .get_value ('listed')#line:510
    if isinstance (O00OO0000O000OO0O ,str ):#line:511
        O00OO00000OOO0OOO [-1 ][O0OO0O0OOO0O0OO0O ]=np .floor (O00OO00000OOO0OOO [-1 ][O00OO0000O000OO0O ])#line:512
    else :#line:513
        O00OO00000OOO0OOO [-1 ][O0OO0O0OOO0O0OO0O ]=np .floor (O00OO0000O000OO0O )#line:514
    gl .set_value ('listed',O00OO00000OOO0OOO )#line:515
    return O0OO0O0OOO0O0OO0O #line:516
def tsminimum (OO000000OO0O00000 ,OO0OO00OO00O00OOO ):#line:519
    O0O0O0O0OOO0000OO ="tsminimum("+OO000000OO0O00000 +","+str (OO0OO00OO00O00OOO )+")"#line:520
    OO0OO00OO00O00OOO =int (round (OO0OO00OO00O00OOO ))#line:521
    if check_dup (O0O0O0O0OOO0000OO ):#line:522
        return O0O0O0O0OOO0000OO #line:523
    O000000O0OOOOO00O =gl .get_value ('listed')#line:524
    if len (O000000O0OOOOO00O )<=OO0OO00OO00O00OOO :#line:525
        print ('The data is insufficient!')#line:526
        OOOO0O0O0O000O000 =pd .DataFrame (index =O000000O0OOOOO00O [-1 ].index ,columns =[O0O0O0O0OOO0000OO ])#line:527
    else :#line:528
        O000OO00O0OOO0OO0 =pd .DataFrame (index =O000000O0OOOOO00O [-1 ].index )#line:529
        for OO0O0O0OO00O0000O in range (1 ,OO0OO00OO00O00OOO +1 ):#line:530
            O00O0O0O00O000OOO =pd .DataFrame (O000000O0OOOOO00O [(-OO0O0O0OO00O0000O )][OO000000OO0O00000 ])#line:531
            O00O0O0O00O000OOO .columns =['c'+str (OO0O0O0OO00O0000O )]#line:532
            O000OO00O0OOO0OO0 =pd .concat ([O000OO00O0OOO0OO0 ,O00O0O0O00O000OOO ['c'+str (OO0O0O0OO00O0000O )]],axis =1 ,join ='outer')#line:533
        OOOO0O0O0O000O000 =pd .DataFrame (O000OO00O0OOO0OO0 .min (axis =1 ,skipna =True ))#line:534
        OOOO0O0O0O000O000 .columns =[O0O0O0O0OOO0000OO ]#line:535
    O000000O0OOOOO00O [-1 ]=pd .concat ([O000000O0OOOOO00O [-1 ],OOOO0O0O0O000O000 ],axis =1 ,join ='outer')#line:536
    gl .set_value ('listed',O000000O0OOOOO00O )#line:537
    return O0O0O0O0OOO0000OO #line:538
def tsmaximum (OO00O0O00O00OO0O0 ,OO0OOO0O0OOO0O00O ):#line:541
    O0OOO0O0OO0OOOOOO ="tsmaximum("+OO00O0O00O00OO0O0 +","+str (OO0OOO0O0OOO0O00O )+")"#line:542
    OO0OOO0O0OOO0O00O =int (round (OO0OOO0O0OOO0O00O ))#line:543
    if check_dup (O0OOO0O0OO0OOOOOO ):#line:544
        return O0OOO0O0OO0OOOOOO #line:545
    O00O00OO0O00O000O =gl .get_value ('listed')#line:546
    if len (O00O00OO0O00O000O )<=OO0OOO0O0OOO0O00O :#line:547
        print ('The data is insufficient!')#line:548
        OOOOO0OOOOO0OOO00 =pd .DataFrame (index =O00O00OO0O00O000O [-1 ].index ,columns =[O0OOO0O0OO0OOOOOO ])#line:549
    else :#line:550
        O0000OOO00000OOO0 =pd .DataFrame (index =O00O00OO0O00O000O [-1 ].index )#line:551
        for OOOO0O0O000O0O000 in range (1 ,OO0OOO0O0OOO0O00O +1 ):#line:552
            O0OO0OO000O0O00OO =pd .DataFrame (O00O00OO0O00O000O [(-OOOO0O0O000O0O000 )][OO00O0O00O00OO0O0 ])#line:553
            O0OO0OO000O0O00OO .columns =['c'+str (OOOO0O0O000O0O000 )]#line:554
            O0000OOO00000OOO0 =pd .concat ([O0000OOO00000OOO0 ,O0OO0OO000O0O00OO ['c'+str (OOOO0O0O000O0O000 )]],axis =1 ,join ='outer')#line:555
        OOOOO0OOOOO0OOO00 =pd .DataFrame (O0000OOO00000OOO0 .max (axis =1 ,skipna =True ))#line:556
        OOOOO0OOOOO0OOO00 .columns =[O0OOO0O0OO0OOOOOO ]#line:557
    O00O00OO0O00O000O [-1 ]=pd .concat ([O00O00OO0O00O000O [-1 ],OOOOO0OOOOO0OOO00 ],axis =1 ,join ='outer')#line:558
    gl .set_value ('listed',O00O00OO0O00O000O )#line:559
    return O0OOO0O0OO0OOOOOO #line:560
def tsrank (O0O0OOO0O00OO00O0 ,OOO0O0O000OOO00OO ):#line:563
    OOO00OOOOOOOO00O0 ="tsrank("+O0O0OOO0O00OO00O0 +","+str (OOO0O0O000OOO00OO )+")"#line:564
    OOO0O0O000OOO00OO =int (round (OOO0O0O000OOO00OO ))#line:565
    if check_dup (OOO00OOOOOOOO00O0 ):#line:566
        return OOO00OOOOOOOO00O0 #line:567
    O0000O00OOOOO0O0O =gl .get_value ('listed')#line:568
    if len (O0000O00OOOOO0O0O )<=OOO0O0O000OOO00OO :#line:569
        print ('The data is insufficient!')#line:570
        O00OO00OO0OOOO00O =pd .DataFrame (index =O0000O00OOOOO0O0O [-1 ].index ,columns =[OOO00OOOOOOOO00O0 ])#line:571
    else :#line:572
        OO0000OOO0O0O00O0 =pd .DataFrame (index =O0000O00OOOOO0O0O [-1 ].index )#line:573
        for OOOOOO00000OO0O00 in range (1 ,OOO0O0O000OOO00OO +1 ):#line:574
            O00O0OOOO00000OOO =pd .DataFrame (O0000O00OOOOO0O0O [(-OOOOOO00000OO0O00 )][O0O0OOO0O00OO00O0 ])#line:575
            O00O0OOOO00000OOO .columns =['c'+str (OOOOOO00000OO0O00 )]#line:576
            OO0000OOO0O0O00O0 =pd .concat ([OO0000OOO0O0O00O0 ,O00O0OOOO00000OOO ['c'+str (OOOOOO00000OO0O00 )]],axis =1 ,join ='outer')#line:577
        O00OO00OO0OOOO00O =pd .DataFrame (OO0000OOO0O0O00O0 .rank (axis =1 )['c1']/OOO0O0O000OOO00OO )#line:578
        O00OO00OO0OOOO00O .columns =[OOO00OOOOOOOO00O0 ]#line:579
    O0000O00OOOOO0O0O [-1 ]=pd .concat ([O0000O00OOOOO0O0O [-1 ],O00OO00OO0OOOO00O ],axis =1 ,join ='outer')#line:580
    gl .set_value ('listed',O0000O00OOOOO0O0O )#line:581
    return OOO00OOOOOOOO00O0 #line:582
def std (OO0O00O0OO0O000O0 ,OO00OOO00O0000O0O ):#line:585
    OOO0OO0O0O000O000 ="std("+OO0O00O0OO0O000O0 +","+str (OO00OOO00O0000O0O )+")"#line:586
    OO00OOO00O0000O0O =int (round (OO00OOO00O0000O0O ))#line:587
    if check_dup (OOO0OO0O0O000O000 ):#line:588
        return OOO0OO0O0O000O000 #line:589
    O0OO0OOO0000OOO0O =gl .get_value ('listed')#line:590
    if len (O0OO0OOO0000OOO0O )<=OO00OOO00O0000O0O :#line:591
        print ('The data is insufficient!')#line:592
        OOO000O00O0O000OO =pd .DataFrame (index =O0OO0OOO0000OOO0O [-1 ].index ,columns =[OOO0OO0O0O000O000 ])#line:593
    else :#line:594
        OO00OOO00OOO0000O =pd .DataFrame (index =O0OO0OOO0000OOO0O [-1 ].index )#line:595
        for O0OOOOO0OOOOO00OO in range (1 ,OO00OOO00O0000O0O +1 ):#line:596
            OO0O0OO00O0OO00O0 =pd .DataFrame (O0OO0OOO0000OOO0O [(-O0OOOOO0OOOOO00OO )][OO0O00O0OO0O000O0 ])#line:597
            OO0O0OO00O0OO00O0 .columns =['c'+str (O0OOOOO0OOOOO00OO )]#line:598
            OO00OOO00OOO0000O =pd .concat ([OO00OOO00OOO0000O ,OO0O0OO00O0OO00O0 ['c'+str (O0OOOOO0OOOOO00OO )]],axis =1 ,join ='outer')#line:599
        OO00OOO00OOO0000O =OO00OOO00OOO0000O .fillna (axis =1 ,method ="ffill")#line:600
        OO00OOO00OOO0000O =OO00OOO00OOO0000O .fillna (axis =1 ,method ="backfill")#line:601
        OOO000O00O0O000OO =pd .DataFrame (OO00OOO00OOO0000O .std (axis =1 ))#line:602
        OOO000O00O0O000OO .columns =[OOO0OO0O0O000O000 ]#line:603
    O0OO0OOO0000OOO0O [-1 ]=pd .concat ([O0OO0OOO0000OOO0O [-1 ],OOO000O00O0O000OO ],axis =1 ,join ='outer')#line:604
    gl .set_value ('listed',O0OO0OOO0000OOO0O )#line:605
    return OOO0OO0O0O000O000 #line:606
def maximum (O0000OO00OO0O000O ,O0OO00O0O0O00O0O0 ):#line:609
    O0O0000O0O0OO00O0 ='maximum'+'('+str (O0000OO00OO0O000O )+','+str (O0OO00O0O0O00O0O0 )+')'#line:612
    if check_dup (O0O0000O0O0OO00O0 ):#line:613
        return O0O0000O0O0OO00O0 #line:614
    OOOOO00O000000O00 =gl .get_value ('listed')#line:615
    if isinstance (O0000OO00OO0O000O ,str )and isinstance (O0OO00O0O0O00O0O0 ,str ):#line:616
        OO000OOO00O0O0O0O =OOOOO00O000000O00 [-1 ][O0000OO00OO0O000O ].fillna (value =-np .inf )#line:618
        O0O0OO000OO0OO0O0 =OOOOO00O000000O00 [-1 ][O0OO00O0O0O00O0O0 ].fillna (value =-np .inf )#line:619
        OOOOO00O000000O00 [-1 ][O0O0000O0O0OO00O0 ]=np .maximum (OO000OOO00O0O0O0O ,O0O0OO000OO0OO0O0 )#line:620
    elif isinstance (O0000OO00OO0O000O ,str ):#line:621
        OO000OOO00O0O0O0O =OOOOO00O000000O00 [-1 ][O0000OO00OO0O000O ].fillna (value =-np .inf )#line:623
        OOOOO00O000000O00 [-1 ][O0O0000O0O0OO00O0 ]=np .maximum (OO000OOO00O0O0O0O ,O0OO00O0O0O00O0O0 )#line:624
    elif isinstance (O0OO00O0O0O00O0O0 ,str ):#line:625
        O0O0OO000OO0OO0O0 =OOOOO00O000000O00 [-1 ][O0OO00O0O0O00O0O0 ].fillna (value =-np .inf )#line:627
        OOOOO00O000000O00 [-1 ][O0O0000O0O0OO00O0 ]=np .maximum (O0O0OO000OO0OO0O0 ,O0000OO00OO0O000O )#line:628
    elif not isinstance (O0000OO00OO0O000O ,str )and not isinstance (O0OO00O0O0O00O0O0 ,str ):#line:629
        OOOOO00O000000O00 [-1 ][O0O0000O0O0OO00O0 ]=np .maximum (O0000OO00OO0O000O ,O0OO00O0O0O00O0O0 )#line:631
    gl .set_value ('listed',OOOOO00O000000O00 )#line:632
    return O0O0000O0O0OO00O0 #line:633
def minimum (OOO0OO0O000O00O0O ,OOOOO0O0O0OO0OO00 ):#line:636
    O00O0O0O0O0O000OO ='minimum'+'('+str (OOO0OO0O000O00O0O )+','+str (OOOOO0O0O0OO0OO00 )+')'#line:639
    if check_dup (O00O0O0O0O0O000OO ):#line:640
        return O00O0O0O0O0O000OO #line:641
    OO0000O0000000O0O =gl .get_value ('listed')#line:642
    if isinstance (OOO0OO0O000O00O0O ,str )and isinstance (OOOOO0O0O0OO0OO00 ,str ):#line:643
        O0O0O0OOOOO0OO0OO =OO0000O0000000O0O [-1 ][OOO0OO0O000O00O0O ].fillna (value =np .inf )#line:645
        OO0OOO0OOOO00O00O =OO0000O0000000O0O [-1 ][OOOOO0O0O0OO0OO00 ].fillna (value =np .inf )#line:646
        OO0000O0000000O0O [-1 ][O00O0O0O0O0O000OO ]=np .minimum (O0O0O0OOOOO0OO0OO ,OO0OOO0OOOO00O00O )#line:647
    elif isinstance (OOO0OO0O000O00O0O ,str ):#line:648
        O0O0O0OOOOO0OO0OO =OO0000O0000000O0O [-1 ][OOO0OO0O000O00O0O ].fillna (value =np .inf )#line:650
        OO0000O0000000O0O [-1 ][O00O0O0O0O0O000OO ]=np .minimum (O0O0O0OOOOO0OO0OO ,OOOOO0O0O0OO0OO00 )#line:651
    elif isinstance (OOOOO0O0O0OO0OO00 ,str ):#line:652
        OO0OOO0OOOO00O00O =OO0000O0000000O0O [-1 ][OOOOO0O0O0OO0OO00 ].fillna (value =np .inf )#line:654
        OO0000O0000000O0O [-1 ][O00O0O0O0O0O000OO ]=np .minimum (OO0OOO0OOOO00O00O ,OOO0OO0O000O00O0O )#line:655
    elif not isinstance (OOO0OO0O000O00O0O ,str )and not isinstance (OOOOO0O0O0OO0OO00 ,str ):#line:656
        OO0000O0000000O0O [-1 ][O00O0O0O0O0O000OO ]=np .minimum (OOO0OO0O000O00O0O ,OOOOO0O0O0OO0OO00 )#line:658
    gl .set_value ('listed',OO0000O0000000O0O )#line:659
    return O00O0O0O0O0O000OO #line:660
def multiminimum (*OO000OOOO0OO0O00O ):#line:663
    O00OOO0O0O00O0O00 =[]#line:664
    O0000O0O00O0O0O0O =[]#line:665
    OOOO0O0OO000O0O0O =gl .get_value ('listed')#line:666
    for OO00OO0OOO0OO0OO0 in OO000OOOO0OO0O00O :#line:667
        if isinstance (OO00OO0OOO0OO0OO0 ,str ):#line:668
            O00O0O0OOOOOO0O0O =OOOO0O0OO000O0O0O [-1 ][OO00OO0OOO0OO0OO0 ].fillna (value =np .inf )#line:669
            O00OOO0O0O00O0O00 .append (O00O0O0OOOOOO0O0O )#line:670
            O0000O0O00O0O0O0O .append (OO00OO0OOO0OO0OO0 )#line:671
        else :#line:672
            O00OOO0O0O00O0O00 .append (OO00OO0OOO0OO0OO0 )#line:673
            O0000O0O00O0O0O0O .append (OO00OO0OOO0OO0OO0 )#line:674
    O00O000OOOOO0O0O0 =''#line:675
    for OOOO00O0OO0000OO0 in range (len (O0000O0O00O0O0O0O )):#line:676
        if OOOO00O0OO0000OO0 !=len (O0000O0O00O0O0O0O )-1 :#line:677
            O00O000OOOOO0O0O0 +=str (O0000O0O00O0O0O0O [OOOO00O0OO0000OO0 ])+','#line:678
        else :#line:679
            O00O000OOOOO0O0O0 +=str (O0000O0O00O0O0O0O [OOOO00O0OO0000OO0 ])#line:680
    O00O000OOOOO0O0O0 ='multiminimum'+'('+O00O000OOOOO0O0O0 +')'#line:681
    if check_dup (O00O000OOOOO0O0O0 ):#line:682
        return O00O000OOOOO0O0O0 #line:683
    OOOO0O0OO000O0O0O [-1 ][O00O000OOOOO0O0O0 ]=O00OOO0O0O00O0O00 [0 ]#line:684
    for OOOO00O0OO0000OO0 in range (len (O00OOO0O0O00O0O00 )):#line:685
        OOOO0O0OO000O0O0O [-1 ][O00O000OOOOO0O0O0 ]=np .minimum (OOOO0O0OO000O0O0O [-1 ][O00O000OOOOO0O0O0 ],O00OOO0O0O00O0O00 [OOOO00O0OO0000OO0 ])#line:686
    gl .set_value ('listed',OOOO0O0OO000O0O0O )#line:687
    return O00O000OOOOO0O0O0 #line:688
def multimaximum (*O000O0O0O00OO00OO ):#line:691
    OOOO0O00000O0O0O0 =[]#line:692
    O000OOO00000OOOOO =[]#line:693
    O00O0000OO00000OO =gl .get_value ('listed')#line:694
    for OOO00OO0OOO00000O in O000O0O0O00OO00OO :#line:695
        if isinstance (OOO00OO0OOO00000O ,str ):#line:696
            OOO0OO0OO00000OOO =O00O0000OO00000OO [-1 ][OOO00OO0OOO00000O ].fillna (value =-np .inf )#line:697
            OOOO0O00000O0O0O0 .append (OOO0OO0OO00000OOO )#line:698
            O000OOO00000OOOOO .append (OOO00OO0OOO00000O )#line:699
        else :#line:700
            OOOO0O00000O0O0O0 .append (OOO00OO0OOO00000O )#line:701
            O000OOO00000OOOOO .append (OOO00OO0OOO00000O )#line:702
    O000O0OO000O00000 =''#line:703
    for OO0O0OOOOOOO0O00O in range (len (O000OOO00000OOOOO )):#line:704
        if OO0O0OOOOOOO0O00O !=len (O000OOO00000OOOOO )-1 :#line:705
            O000O0OO000O00000 +=str (O000OOO00000OOOOO [OO0O0OOOOOOO0O00O ])+','#line:706
        else :#line:707
            O000O0OO000O00000 +=str (O000OOO00000OOOOO [OO0O0OOOOOOO0O00O ])#line:708
    O000O0OO000O00000 ='multimaximum'+'('+O000O0OO000O00000 +')'#line:709
    if check_dup (O000O0OO000O00000 ):#line:710
        return O000O0OO000O00000 #line:711
    O00O0000OO00000OO [-1 ][O000O0OO000O00000 ]=OOOO0O00000O0O0O0 [0 ]#line:712
    for OO0O0OOOOOOO0O00O in range (len (OOOO0O00000O0O0O0 )):#line:713
        O00O0000OO00000OO [-1 ][O000O0OO000O00000 ]=np .maximum (O00O0000OO00000OO [-1 ][O000O0OO000O00000 ],OOOO0O00000O0O0O0 [OO0O0OOOOOOO0O00O ])#line:714
    gl .set_value ('listed',O00O0000OO00000OO )#line:715
    return O000O0OO000O00000 #line:716
def summation (OOOO0OO000O0OOO0O ,O00OOO00O00O000O0 ):#line:719
    OOO00OOOO0O00OO00 ='summation'+'('+OOOO0OO000O0OOO0O +','+str (O00OOO00O00O000O0 )+')'#line:722
    O00OOO00O00O000O0 =int (round (O00OOO00O00O000O0 ))#line:723
    if check_dup (OOO00OOOO0O00OO00 ):#line:724
        return OOO00OOOO0O00OO00 #line:725
    O0O000OO00OOOO000 =gl .get_value ('listed')#line:726
    if len (O0O000OO00OOOO000 )<O00OOO00O00O000O0 :#line:727
        print ('The data is insufficient!')#line:728
        O00O000O0OO00O0OO =pd .DataFrame (index =O0O000OO00OOOO000 [-1 ].index ,columns =[OOO00OOOO0O00OO00 ])#line:729
        O0O000OO00OOOO000 [-1 ]=pd .concat ([O0O000OO00OOOO000 [-1 ],O00O000O0OO00O0OO ],axis =1 ,join ='outer')#line:730
    else :#line:731
        O0O000OO00OOOO000 [-1 ][OOO00OOOO0O00OO00 ]=O0O000OO00OOOO000 [-1 ][OOOO0OO000O0OOO0O ]#line:732
        for OO000000OO00OOOOO in range (2 ,O00OOO00O00O000O0 +1 ):#line:733
            O0O000OO00OOOO000 [-1 ][OOO00OOOO0O00OO00 ]+=O0O000OO00OOOO000 [-OO000000OO00OOOOO ][OOOO0OO000O0OOO0O ]#line:734
    gl .set_value ('listed',O0O000OO00OOOO000 )#line:735
    return OOO00OOOO0O00OO00 #line:736
def product (O00OOOOO00O0O0OO0 ,O0OO0OO00000OOO0O ):#line:739
    OOO0OO0O00O00000O ='product'+'('+O00OOOOO00O0O0OO0 +','+str (O0OO0OO00000OOO0O )+')'#line:742
    O0OO0OO00000OOO0O =int (round (O0OO0OO00000OOO0O ))#line:743
    if check_dup (OOO0OO0O00O00000O ):#line:744
        return OOO0OO0O00O00000O #line:745
    OO0OOOO00OO00O000 =gl .get_value ('listed')#line:746
    if len (OO0OOOO00OO00O000 )<O0OO0OO00000OOO0O :#line:747
        print ('The data is insufficient!')#line:748
        OO000OO0OO0O0OOOO =pd .DataFrame (index =OO0OOOO00OO00O000 [-1 ].index ,columns =[OOO0OO0O00O00000O ])#line:749
        OO0OOOO00OO00O000 [-1 ]=pd .concat ([OO0OOOO00OO00O000 [-1 ],OO000OO0OO0O0OOOO ],axis =1 ,join ='outer')#line:750
    else :#line:751
        OO0OOOO00OO00O000 [-1 ][OOO0OO0O00O00000O ]=OO0OOOO00OO00O000 [-1 ][O00OOOOO00O0O0OO0 ]#line:752
        for O00O00O0000000000 in range (2 ,O0OO0OO00000OOO0O +1 ):#line:753
            OO0OOOO00OO00O000 [-1 ][OOO0OO0O00O00000O ]*=OO0OOOO00OO00O000 [-O00O00O0000000000 ][O00OOOOO00O0O0OO0 ]#line:754
    gl .set_value ('listed',OO0OOOO00OO00O000 )#line:755
    return OOO0OO0O00O00000O #line:756
def scale (O000OOOO0OOO0000O ):#line:759
    OOOOO0OO00OO0O0O0 ="scale("+O000OOOO0OOO0000O +")"#line:760
    if check_dup (OOOOO0OO00OO0O0O0 ):#line:761
        return OOOOO0OO00OO0O0O0 #line:762
    OO0OO0000O0O0O000 =gl .get_value ('listed')#line:763
    OO0OOOO00O000000O =abs (OO0OO0000O0O0O000 [-1 ][O000OOOO0OOO0000O ]).sum ()#line:764
    OO0OO0000O0O0O000 [-1 ][OOOOO0OO00OO0O0O0 ]=OO0OO0000O0O0O000 [-1 ][O000OOOO0OOO0000O ]/OO0OOOO00O000000O #line:765
    gl .set_value ('listed',OO0OO0000O0O0O000 )#line:766
    return OOOOO0OO00OO0O0O0 #line:767
def tsmean (OOOOOO0O0OO0O0O0O ,OO000O00OOOOOO00O ):#line:770
    OO0O00O00O000O0OO ="tsmean("+OOOOOO0O0OO0O0O0O +","+str (OO000O00OOOOOO00O )+")"#line:771
    OO000O00OOOOOO00O =int (round (OO000O00OOOOOO00O ))#line:772
    if check_dup (OO0O00O00O000O0OO ):#line:773
        return OO0O00O00O000O0OO #line:774
    O00OOO0O00OO0OOO0 =gl .get_value ('listed')#line:775
    if len (O00OOO0O00OO0OOO0 )<=OO000O00OOOOOO00O :#line:776
        print ('The data is insufficient!')#line:777
        OOO00O0OO00OOOOO0 =pd .DataFrame (index =O00OOO0O00OO0OOO0 [-1 ].index ,columns =[OO0O00O00O000O0OO ])#line:778
    else :#line:779
        O0OOOO00O0OO000OO =pd .DataFrame (index =O00OOO0O00OO0OOO0 [-1 ].index )#line:780
        for OOO0OO00OOOO0O0O0 in range (1 ,OO000O00OOOOOO00O +1 ):#line:781
            O0OOOOO0OOO0OO0OO =pd .DataFrame (O00OOO0O00OO0OOO0 [(-OOO0OO00OOOO0O0O0 )][OOOOOO0O0OO0O0O0O ])#line:782
            O0OOOOO0OOO0OO0OO .columns =['c'+str (OOO0OO00OOOO0O0O0 )]#line:783
            O0OOOO00O0OO000OO =pd .concat ([O0OOOO00O0OO000OO ,O0OOOOO0OOO0OO0OO ['c'+str (OOO0OO00OOOO0O0O0 )]],axis =1 ,join ='outer')#line:784
        OOO00O0OO00OOOOO0 =pd .DataFrame (O0OOOO00O0OO000OO .mean (axis =1 ,skipna =True ))#line:785
        OOO00O0OO00OOOOO0 .columns =[OO0O00O00O000O0OO ]#line:786
    O00OOO0O00OO0OOO0 [-1 ]=pd .concat ([O00OOO0O00OO0OOO0 [-1 ],OOO00O0OO00OOOOO0 ],axis =1 ,join ='outer')#line:787
    gl .set_value ('listed',O00OOO0O00OO0OOO0 )#line:788
    return OO0O00O00O000O0OO #line:789
def argminimum (O0O0000OO0OO0O0O0 ,OOOOOO000000O0OO0 ):#line:792
    O0O0O00OOOOO00OOO ="argminimum("+O0O0000OO0OO0O0O0 +","+str (OOOOOO000000O0OO0 )+")"#line:795
    OOOOOO000000O0OO0 =int (round (OOOOOO000000O0OO0 ))#line:796
    if check_dup (O0O0O00OOOOO00OOO ):#line:797
        return O0O0O00OOOOO00OOO #line:798
    OOOOO000OOOOO000O =gl .get_value ('listed')#line:799
    if len (OOOOO000OOOOO000O )<=OOOOOO000000O0OO0 :#line:800
        print ('The data is insufficient!')#line:801
        OOO00O0O00OO0OOO0 =pd .DataFrame (index =OOOOO000OOOOO000O [-1 ].index ,columns =[O0O0O00OOOOO00OOO ])#line:802
        OOOOO000OOOOO000O [-1 ]=pd .concat ([OOOOO000OOOOO000O [-1 ],OOO00O0O00OO0OOO0 ],axis =1 ,join ='outer')#line:803
    else :#line:804
        OO0O0000000OO0O0O =pd .DataFrame (index =OOOOO000OOOOO000O [-1 ].index )#line:805
        for OO0OOO000OOOO00OO in range (1 ,OOOOOO000000O0OO0 +1 ):#line:806
            OO0O00OO0O0OOOO0O =pd .DataFrame (OOOOO000OOOOO000O [(-OO0OOO000OOOO00OO )][O0O0000OO0OO0O0O0 ])#line:807
            OO0O00OO0O0OOOO0O .columns =['c'+str (OO0OOO000OOOO00OO )]#line:808
            OO0O0000000OO0O0O =pd .concat ([OO0O0000000OO0O0O ,OO0O00OO0O0OOOO0O ['c'+str (OO0OOO000OOOO00OO )]],axis =1 ,join_axes =[OO0O0000000OO0O0O .index ])#line:809
        OO0O00O0000OO000O =OO0O0000000OO0O0O .dropna (axis =0 ,how ='all')#line:810
        OO0O00O0000OO000O =OO0O0000000OO0O0O .fillna (value =np .inf )#line:811
        O000OOOOOOO00OO00 =[]#line:812
        for OO0OOO000OOOO00OO in range (1 ,OOOOOO000000O0OO0 +1 ):#line:813
            OOOO00O0O000O000O =OO0O00O0000OO000O ['c'+str (OO0OOO000OOOO00OO )]#line:814
            OOOO00OO0OOO0O0O0 =OOOO00O0O000O000O .tolist ()#line:815
            O000OOOOOOO00OO00 .append (OOOO00OO0OOO0O0O0 )#line:816
        OOOOO000OOOOO000O [-1 ][O0O0O00OOOOO00OOO ]=np .argmin (O000OOOOOOO00OO00 ,axis =0 )+1 #line:817
    gl .set_value ('listed',OOOOO000OOOOO000O )#line:818
    return O0O0O00OOOOO00OOO #line:819
def argmaximum (O00OO00OOOOOO0OO0 ,O0000OO0O0O00O0O0 ):#line:822
    OO0000OOOO0000O00 ="argmaximum("+O00OO00OOOOOO0OO0 +","+str (O0000OO0O0O00O0O0 )+")"#line:825
    O0000OO0O0O00O0O0 =int (round (O0000OO0O0O00O0O0 ))#line:826
    if check_dup (OO0000OOOO0000O00 ):#line:827
        return OO0000OOOO0000O00 #line:828
    O000O0OOO00OOOOO0 =gl .get_value ('listed')#line:829
    if len (O000O0OOO00OOOOO0 )<=O0000OO0O0O00O0O0 :#line:830
        print ('The data is insufficient!')#line:831
        O0OO0000O0O000O00 =pd .DataFrame (index =O000O0OOO00OOOOO0 [-1 ].index ,columns =[OO0000OOOO0000O00 ])#line:832
        O000O0OOO00OOOOO0 [-1 ]=pd .concat ([O000O0OOO00OOOOO0 [-1 ],O0OO0000O0O000O00 ],axis =1 ,join ='outer')#line:833
    else :#line:834
        OO0O0OO0OOOO0O00O =pd .DataFrame (index =O000O0OOO00OOOOO0 [-1 ].index )#line:835
        for O0OOOO0OOOO0O0O0O in range (1 ,O0000OO0O0O00O0O0 +1 ):#line:836
            OOOO000O00O00OO0O =pd .DataFrame (O000O0OOO00OOOOO0 [(-O0OOOO0OOOO0O0O0O )][O00OO00OOOOOO0OO0 ])#line:837
            OOOO000O00O00OO0O .columns =['c'+str (O0OOOO0OOOO0O0O0O )]#line:838
            OO0O0OO0OOOO0O00O =pd .concat ([OO0O0OO0OOOO0O00O ,OOOO000O00O00OO0O ['c'+str (O0OOOO0OOOO0O0O0O )]],axis =1 ,join_axes =[OO0O0OO0OOOO0O00O .index ])#line:839
        O00O0OOOO0O0O00OO =OO0O0OO0OOOO0O00O .dropna (axis =0 ,how ='all')#line:840
        O00O0OOOO0O0O00OO =OO0O0OO0OOOO0O00O .fillna (value =np .inf )#line:841
        OOOOOOOO0OO0O0000 =[]#line:842
        for O0OOOO0OOOO0O0O0O in range (1 ,O0000OO0O0O00O0O0 +1 ):#line:843
            O00OOOOO0OOOOOOO0 =O00O0OOOO0O0O00OO ['c'+str (O0OOOO0OOOO0O0O0O )]#line:844
            OOO000O00O00O000O =O00OOOOO0OOOOOOO0 .tolist ()#line:845
            OOOOOOOO0OO0O0000 .append (OOO000O00O00O000O )#line:846
        O000O0OOO00OOOOO0 [-1 ][OO0000OOOO0000O00 ]=np .argmax (OOOOOOOO0OO0O0000 ,axis =0 )+1 #line:847
    gl .set_value ('listed',O000O0OOO00OOOOO0 )#line:848
    return OO0000OOOO0000O00 #line:849
def decayexp (OOOOOOOOOOOO00OO0 ,OOO0OOOOOOOO00000 ,O0O000OOO00000O0O ):#line:852
    O00OOOOO000O00O00 ='decayexp'+'('+OOOOOOOOOOOO00OO0 +','+str (OOO0OOOOOOOO00000 )+','+str (O0O000OOO00000O0O )+')'#line:853
    O0O000OOO00000O0O =int (round (O0O000OOO00000O0O ))#line:854
    if check_dup (O00OOOOO000O00O00 ):#line:855
        return O00OOOOO000O00O00 #line:856
    O00000000OOO000OO =gl .get_value ('listed')#line:857
    if len (O00000000OOO000OO )<O0O000OOO00000O0O :#line:858
        print ('The data is insufficient!')#line:859
        OO0O00O0O00OO000O =pd .DataFrame (index =O00000000OOO000OO [-1 ].index ,columns =[O00OOOOO000O00O00 ])#line:860
        O00000000OOO000OO [-1 ]=pd .concat ([O00000000OOO000OO [-1 ],OO0O00O0O00OO000O ],axis =1 ,join ='outer')#line:861
    else :#line:862
        O000OOO0OOOO0O000 =1 #line:863
        O00000000OOO000OO [-1 ][O00OOOOO000O00O00 ]=O00000000OOO000OO [-1 ][OOOOOOOOOOOO00OO0 ]#line:864
        for O000O0OO0OOO000OO in range (2 ,O0O000OOO00000O0O +1 ):#line:865
            O00000000OOO000OO [-1 ][O00OOOOO000O00O00 ]+=O00000000OOO000OO [-O000O0OO0OOO000OO ][OOOOOOOOOOOO00OO0 ]*OOO0OOOOOOOO00000 **(O000O0OO0OOO000OO -1 )#line:866
            O000OOO0OOOO0O000 =O000OOO0OOOO0O000 +OOO0OOOOOOOO00000 **(O000O0OO0OOO000OO -1 )#line:867
        O00000000OOO000OO [-1 ][O00OOOOO000O00O00 ]=O00000000OOO000OO [-1 ][O00OOOOO000O00O00 ]/O000OOO0OOOO0O000 #line:868
    gl .set_value ('listed',O00000000OOO000OO )#line:869
    return O00OOOOO000O00O00 #line:870
def decaylinear (O0OOO000O0OO0O0O0 ,OOOO0O0OOOO00O0O0 ):#line:873
    O000O00OO000OO00O ='decaylinear'+'('+O0OOO000O0OO0O0O0 +','+str (OOOO0O0OOOO00O0O0 )+')'#line:874
    OOOO0O0OOOO00O0O0 =int (round (OOOO0O0OOOO00O0O0 ))#line:875
    if check_dup (O000O00OO000OO00O ):#line:876
        return O000O00OO000OO00O #line:877
    O0O00OO0OOOO0O0OO =gl .get_value ('listed')#line:878
    if len (O0O00OO0OOOO0O0OO )<OOOO0O0OOOO00O0O0 :#line:879
        print ('The data is insufficient!')#line:880
        OOOOO0O0OO0OOO00O =pd .DataFrame (index =O0O00OO0OOOO0O0OO [-1 ].index ,columns =[O000O00OO000OO00O ])#line:881
        O0O00OO0OOOO0O0OO [-1 ]=pd .concat ([O0O00OO0OOOO0O0OO [-1 ],OOOOO0O0OO0OOO00O ],axis =1 ,join ='outer')#line:882
    else :#line:883
        O0000OO000OOO000O =OOOO0O0OOOO00O0O0 #line:884
        O0O00OO0OOOO0O0OO [-1 ][O000O00OO000OO00O ]=O0O00OO0OOOO0O0OO [-1 ][O0OOO000O0OO0O0O0 ]*OOOO0O0OOOO00O0O0 #line:885
        for OO000O00OOOOO0OO0 in range (2 ,OOOO0O0OOOO00O0O0 +1 ):#line:886
            O0O00OO0OOOO0O0OO [-1 ][O000O00OO000OO00O ]+=O0O00OO0OOOO0O0OO [-OO000O00OOOOO0OO0 ][O0OOO000O0OO0O0O0 ]*(OOOO0O0OOOO00O0O0 -OO000O00OOOOO0OO0 +1 )#line:887
            O0000OO000OOO000O =O0000OO000OOO000O +(OOOO0O0OOOO00O0O0 -OO000O00OOOOO0OO0 +1 )#line:888
        O0O00OO0OOOO0O0OO [-1 ][O000O00OO000OO00O ]=O0O00OO0OOOO0O0OO [-1 ][O000O00OO000OO00O ]/O0000OO000OOO000O #line:889
    gl .set_value ('listed',O0O00OO0OOOO0O0OO )#line:890
    return O000O00OO000OO00O #line:891
def tsregression (O000OO00OOOOO0OOO ,O0OO0O00OO00O0OO0 ,O0000O0OO0O00O0O0 ,OO0OO0O0000O0OOOO ,OO00OO00O0OOO000O ):#line:894
    O0OO0O0OOOOO0O0OO ="tsregression("+O000OO00OOOOO0OOO +","+O0OO0O00OO00O0OO0 +","+str (O0000O0OO0O00O0O0 )+","+str (OO0OO0O0000O0OOOO )+","+str (OO00OO00O0OOO000O )+")"#line:899
    O0000O0OO0O00O0O0 =int (round (O0000O0OO0O00O0O0 ))#line:900
    OO0OO0O0000O0OOOO =int (round (OO0OO0O0000O0OOOO ))#line:901
    if check_dup (O0OO0O0OOOOO0O0OO ):#line:902
        return O0OO0O0OOOOO0O0OO #line:903
    OOO0O0OOO00O00O0O =gl .get_value ('listed')#line:904
    if len (OOO0O0OOO00O00O0O )<(O0000O0OO0O00O0O0 +OO0OO0O0000O0OOOO ):#line:905
        print ('The data is insufficient!')#line:906
        O0O0000O000OOOO0O =pd .DataFrame (index =OOO0O0OOO00O00O0O [-1 ].index ,columns =[O0OO0O0OOOOO0O0OO ])#line:907
    else :#line:908
        OO00O0000O0O00000 =pd .DataFrame (index =OOO0O0OOO00O00O0O [-1 ].index )#line:909
        for OOOO00O00000O0OOO in range (1 ,O0000O0OO0O00O0O0 +1 ):#line:910
            OOO000O0O00OO00OO =pd .DataFrame (OOO0O0OOO00O00O0O [(-OOOO00O00000O0OOO )][O000OO00OOOOO0OOO ])#line:911
            OOO000O0O00OO00OO .columns =['cy'+str (OOOO00O00000O0OOO )]#line:912
            OOO000O0O00OO00OO =OOO000O0O00OO00OO .dropna (axis =0 ,how ='any')#line:913
            OO00O0000O0O00000 =pd .concat ([OO00O0000O0O00000 ,OOO000O0O00OO00OO ],axis =1 ,join ='inner')#line:914
            O0O00OOO0O0O0OO00 =pd .DataFrame (OOO0O0OOO00O00O0O [(-OOOO00O00000O0OOO -OO0OO0O0000O0OOOO )][O0OO0O00OO00O0OO0 ])#line:915
            O0O00OOO0O0O0OO00 .columns =['cx'+str (OOOO00O00000O0OOO )]#line:916
            O0O00OOO0O0O0OO00 =O0O00OOO0O0O0OO00 .dropna (axis =0 ,how ='any')#line:917
            OO00O0000O0O00000 =pd .concat ([OO00O0000O0O00000 ,O0O00OOO0O0O0OO00 ],axis =1 ,join ='inner')#line:918
        OOOO0O0000O0O0OOO =len (OO00O0000O0O00000 )#line:919
        O00OOO000O00OO0O0 =np .array (OO00O0000O0O00000 [['cy'+str (OO0O00O00OOOO000O )for OO0O00O00OOOO000O in range (1 ,O0000O0OO0O00O0O0 +1 )]])#line:920
        O00OO0OO0OO0OOO0O =np .array (OO00O0000O0O00000 [['cx'+str (O00O0O0000OOO0O00 )for O00O0O0000OOO0O00 in range (1 ,O0000O0OO0O00O0O0 +1 )]])#line:921
        O0OO0OO00O00O0OOO =[]#line:922
        OOO0O0OO00OOO00O0 =[]#line:923
        O0O00OOOO00000000 =[]#line:924
        OOO00OOOOO0OO0O00 =[]#line:925
        for OOOO00O00000O0OOO in range (OOOO0O0000O0O0OOO ):#line:926
            O0OO0O00O0O0O0OO0 =O00OO0OO0OO0OOO0O [OOOO00O00000O0OOO ,:].reshape (O0000O0OO0O00O0O0 ,1 )#line:927
            O0OOO0000O00000O0 =O00OOO000O00OO0O0 [OOOO00O00000O0OOO ,:].reshape (O0000O0OO0O00O0O0 ,1 )#line:928
            OO0O0OO0O000O000O =LinearRegression ().fit (O0OO0O00O0O0O0OO0 ,O0OOO0000O00000O0 )#line:929
            OOO0O0OO00OOO00O0 .append (OO0O0OO0O000O000O .intercept_ [0 ])#line:930
            O0O00OOOO00000000 .append (OO0O0OO0O000O000O .coef_ [0 ])#line:931
            O0O0OO00000O0O00O =OO0O0OO0O000O000O .predict (O0OO0O00O0O0O0OO0 )[0 ]#line:932
            O000O0OO0OO0O000O =O00OOO000O00OO0O0 [OOOO00O00000O0OOO ,0 ]#line:933
            O0OO0OO00O00O0OOO .append (O000O0OO0OO0O000O -O0O0OO00000O0O00O )#line:934
            OOO00OOOOO0OO0O00 .append (O0O0OO00000O0O00O )#line:935
        if OO00OO00O0OOO000O ==0 :#line:936
            O0O0000O000OOOO0O =pd .DataFrame (O0OO0OO00O00O0OOO ,index =OO00O0000O0O00000 .index ,columns =[O0OO0O0OOOOO0O0OO ])#line:937
        elif OO00OO00O0OOO000O ==1 :#line:938
            O0O0000O000OOOO0O =pd .DataFrame (OOO0O0OO00OOO00O0 ,index =OO00O0000O0O00000 .index ,columns =[O0OO0O0OOOOO0O0OO ])#line:939
        elif OO00OO00O0OOO000O ==2 :#line:940
            O0O0000O000OOOO0O =pd .DataFrame (O0O00OOOO00000000 ,index =OO00O0000O0O00000 .index ,columns =[O0OO0O0OOOOO0O0OO ])#line:941
        elif OO00OO00O0OOO000O ==3 :#line:942
            O0O0000O000OOOO0O =pd .DataFrame (OOO00OOOOO0OO0O00 ,index =OO00O0000O0O00000 .index ,columns =[O0OO0O0OOOOO0O0OO ])#line:943
        else :#line:944
            print ('The value of retval is invalid!')#line:945
            O0O0000O000OOOO0O =pd .DataFrame (index =OOO0O0OOO00O00O0O [-1 ].index ,columns =[O0OO0O0OOOOO0O0OO ])#line:946
    OOO0O0OOO00O00O0O [-1 ]=pd .concat ([OOO0O0OOO00O00O0O [-1 ],O0O0000O000OOOO0O ],axis =1 ,join ='outer')#line:947
    gl .set_value ('listed',OOO0O0OOO00O00O0O )#line:948
    return O0OO0O0OOOOO0O0OO #line:949
def returns ():#line:951
    OOOO0O00OOOO00000 ='returns()'#line:952
    if check_dup (OOOO0O00OOOO00000 ):#line:953
        return OOOO0O00OOOO00000 #line:954
    OO0O0000O00O0000O =gl .get_value ('listed')#line:955
    if len (OO0O0000O00O0000O )<=2 :#line:956
        print ('The data is insufficient!')#line:957
        OO0O0000O00O0000O [-1 ][OOOO0O00OOOO00000 ]=pd .Series (index =OO0O0000O00O0000O [-1 ].index )#line:958
    else :#line:959
        OO0OOO00O0O0O0O0O =OO0O0000O00O0000O [-1 ]['close()']#line:960
        O0OO00O00000OO0OO =OO0O0000O00O0000O [-2 ]['close()']#line:961
        OO0O000OO00O00O00 =pd .concat ([OO0OOO00O0O0O0O0O ,O0OO00O00000OO0OO ],axis =1 ,join ='inner')#line:962
        OO0O000OO00O00O00 =OO0O000OO00O00O00 .dropna (axis =0 ,how ="any")#line:963
        OO0O000OO00O00O00 .columns =['c1','c2']#line:964
        OO0O0000O00O0000O [-1 ][OOOO0O00OOOO00000 ]=(OO0O000OO00O00O00 ['c1']-OO0O000OO00O00O00 ['c2'])/OO0O000OO00O00O00 ['c2']#line:965
    gl .set_value ('listed',OO0O0000O00O0000O )#line:966
    return OOOO0O00OOOO00000 #line:967
def counttt (O000000OO00O0O000 ,OO00O00OO0O0O00O0 ):#line:970
    OO00O00OO0O0O00O0 =int (round (OO00O00OO0O0O00O0 ))#line:971
    OO0OOOO000O0OO000 ='counttt('+O000000OO00O0O000 +','+str (OO00O00OO0O0O00O0 )+')'#line:972
    if check_dup (OO0OOOO000O0OO000 ):#line:973
        return OO0OOOO000O0OO000 #line:974
    OOOO00000OO0OO000 =gl .get_value ('listed')#line:975
    if len (OOOO00000OO0OO000 )<=OO00O00OO0O0O00O0 :#line:976
        print ('The data is insufficient!')#line:977
        OOOO00000OO0OO000 [-1 ][OO0OOOO000O0OO000 ]=pd .Series (index =OOOO00000OO0OO000 [-1 ].index )#line:978
    else :#line:979
        OOOO00000OO0OO000 [-1 ][OO0OOOO000O0OO000 ]=0 #line:980
        for OO0OO00O00OO00O00 in range (1 ,OO00O00OO0O0O00O0 +1 ):#line:981
            O0O0OO0000OO00000 =notequal (OOOO00000OO0OO000 [-OO0OO00O00OO00O00 ][O000000OO00O0O000 ],0 )#line:982
            O0O0OO0000OO00000 =OOOO00000OO0OO000 [-OO0OO00O00OO00O00 ][O000000OO00O0O000 ]#line:983
            OOOO00000OO0OO000 [-1 ][OO0OOOO000O0OO000 ]+=O0O0OO0000OO00000 #line:984
    gl .set_value ('listed',OOOO00000OO0OO000 )#line:985
    return OO0OOOO000O0OO000 #line:986
def wma (O0O00OOOOO0OOO0OO ,OO0OOO000O00O0OOO ):#line:989
    OOOO0O0O0OO00000O ='wma'+'('+O0O00OOOOO0OOO0OO +','+str (OO0OOO000O00O0OOO )+')'#line:991
    OO0OOO000O00O0OOO =int (round (OO0OOO000O00O0OOO ))#line:992
    if check_dup (OOOO0O0O0OO00000O ):#line:993
        return OOOO0O0O0OO00000O #line:994
    OOOO0000OO00OOOO0 =gl .get_value ('listed')#line:995
    if len (OOOO0000OO00OOOO0 )<OO0OOO000O00O0OOO :#line:996
        print ('The data is insufficient!')#line:997
        OO00O000O000OOO0O =pd .DataFrame (index =OOOO0000OO00OOOO0 [-1 ].index ,columns =[OOOO0O0O0OO00000O ])#line:998
        OOOO0000OO00OOOO0 [-1 ]=pd .concat ([OOOO0000OO00OOOO0 [-1 ],OO00O000O000OOO0O ],axis =1 ,join ='outer')#line:999
    else :#line:1000
        OOOO0000OO00OOOO0 [-1 ][OOOO0O0O0OO00000O ]=OOOO0000OO00OOOO0 [-1 ][O0O00OOOOO0OOO0OO ]*0.9 *0 #line:1001
        for O00OO0O0000OOO0OO in range (2 ,OO0OOO000O00O0OOO +1 ):#line:1002
            OOOO0000OO00OOOO0 [-1 ][OOOO0O0O0OO00000O ]=OOOO0000OO00OOOO0 [-1 ][OOOO0O0O0OO00000O ]+OOOO0000OO00OOOO0 [-O00OO0O0000OOO0OO ][O0O00OOOOO0OOO0OO ]*0.9 *(O00OO0O0000OOO0OO -1 )#line:1003
    gl .set_value ('listed',OOOO0000OO00OOOO0 )#line:1004
    return OOOO0O0O0OO00000O #line:1005
def sma (OOOO00OOO0OO00000 ,OOOOO0O0OO0OOOOOO ,O0O000000OO0OO000 ):#line:1008
    OOO0O000000000O00 ='sma'+'('+OOOO00OOO0OO00000 +','+str (OOOOO0O0OO0OOOOOO )+','+str (O0O000000OO0OO000 )+')'#line:1009
    OOOOO0O0OO0OOOOOO =int (round (OOOOO0O0OO0OOOOOO ))#line:1010
    O0O000000OO0OO000 =int (round (O0O000000OO0OO000 ))#line:1011
    if check_dup (OOO0O000000000O00 ):#line:1012
        return OOO0O000000000O00 #line:1013
    OOO0O0O0O000OO0O0 =gl .get_value ('listed')#line:1014
    if len (OOO0O0O0O000OO0O0 )<=OOOOO0O0OO0OOOOOO :#line:1015
        print ('The data is insufficient!')#line:1016
        OOO00000O0O0O0OO0 =pd .DataFrame (index =OOO0O0O0O000OO0O0 [-1 ].index ,columns =[OOO0O000000000O00 ])#line:1017
        OOO0O0O0O000OO0O0 [-1 ]=pd .concat ([OOO0O0O0O000OO0O0 [-1 ],OOO00000O0O0O0OO0 ],axis =1 ,join ='outer')#line:1018
    else :#line:1019
        OOO0O0O0O000OO0O0 [-(OOOOO0O0OO0OOOOOO +1 )][OOO0O000000000O00 ]=OOO0O0O0O000OO0O0 [-(OOOOO0O0OO0OOOOOO +1 )][OOOO00OOO0OO00000 ]#line:1020
        O0O0O00OOOO0O0OOO =[O0O00OO00000O00O0 for O0O00OO00000O00O0 in range (1 ,OOOOO0O0OO0OOOOOO +1 )]#line:1021
        O0O0O00OOOO0O0OOO .reverse ()#line:1022
        for O0OO000O000OOO000 in O0O0O00OOOO0O0OOO :#line:1023
            OOO0O0O0O000OO0O0 [-O0OO000O000OOO000 ][OOO0O000000000O00 ]=OOO0O0O0O000OO0O0 [-O0OO000O000OOO000 ][OOOO00OOO0OO00000 ]*O0O000000OO0OO000 /OOOOO0O0OO0OOOOOO +OOO0O0O0O000OO0O0 [-(O0OO000O000OOO000 +1 )][OOO0O000000000O00 ]*(OOOOO0O0OO0OOOOOO -O0O000000OO0OO000 )/OOOOO0O0OO0OOOOOO #line:1024
    gl .set_value ('listed',OOO0O0O0O000OO0O0 )#line:1025
    return OOO0O000000000O00 #line:1026
def sequence (OO00O00OOOO0O0OOO ):#line:1029
    O00OOOO0000000O0O ="sequence("+str (OO00O00OOOO0O0OOO )+")"#line:1030
    OO00O00OOOO0O0OOO =int (round (OO00O00OOOO0O0OOO ))#line:1031
    if check_dup (O00OOOO0000000O0O ):#line:1032
        return O00OOOO0000000O0O #line:1033
    OOOOOO000OO00OO0O =gl .get_value ('listed')#line:1034
    if len (OOOOOO000OO00OO0O )<OO00O00OOOO0O0OOO :#line:1035
        print ('The data is insufficient!')#line:1036
        OOOOOO000OO00OO0O [-1 ][O00OOOO0000000O0O ]=np .nan #line:1037
    else :#line:1038
        for OO0000OO0O0OOOO00 in range (1 ,OO00O00OOOO0O0OOO +1 ):#line:1039
            OOOOOO000OO00OO0O [-OO0000OO0O0OOOO00 ][O00OOOO0000000O0O ]=OO0000OO0O0OOOO00 #line:1040
    gl .set_value ('listed',OOOOOO000OO00OO0O )#line:1041
    return O00OOOO0000000O0O #line:1042
def regbeta (OOO0O0OO000OOOO00 ,O00000O0O0O0OO0OO ,O00O000O0O000OO00 ):#line:1045
    O00O000O0O000OO00 =int (round (O00O000O0O000OO00 ))#line:1046
    OO0OO00O000OO0O0O ="regbeta("+OOO0O0OO000OOOO00 +","+O00000O0O0O0OO0OO +")"#line:1047
    if check_dup (OO0OO00O000OO0O0O ):#line:1048
        return OO0OO00O000OO0O0O #line:1049
    O00OOO0O00O00OOO0 =tsregression (OOO0O0OO000OOOO00 ,O00000O0O0O0OO0OO ,O00O000O0O000OO00 ,0 ,2 )#line:1050
    OO00O0OO0O0O0O0O0 =gl .get_value ('listed')#line:1051
    OO00O0OO0O0O0O0O0 [-1 ][OO0OO00O000OO0O0O ]=OO00O0OO0O0O0O0O0 [-1 ][O00OOO0O00O00OOO0 ]#line:1052
    return OO0OO00O000OO0O0O #line:1053
def condition (OO0OO0OO0OO0OO0OO ,O00O0OO0OOOOOO0OO ,OOOO0O0O0O0OOOO00 ):#line:1061
    O00O000O0O0O00O0O ="condition("+str (OO0OO0OO0OO0OO0OO )+","+str (O00O0OO0OOOOOO0OO )+","+str (OOOO0O0O0O0OOOO00 )+")"#line:1062
    O000O0O0OOO0OOOO0 =gl .get_value ('listed')#line:1063
    if check_dup (O00O000O0O0O00O0O ):#line:1064
        return O00O000O0O0O00O0O #line:1065
    OOO0O0O000OOO0O0O =lambda O000O00000O00O00O :O000O00000O00O00O [0 ]if O000O00000O00O00O [2 ]else O000O00000O00O00O [1 ]#line:1066
    O0OOO0O00OOO00000 =notequal (OO0OO0OO0OO0OO0OO ,0 )#line:1067
    OOO00OO0O0O00O0O0 =O000O0O0OOO0OOOO0 [-1 ][O0OOO0O00OOO00000 ]#line:1068
    if isinstance (O00O0OO0OOOOOO0OO ,str )and isinstance (OOOO0O0O0O0OOOO00 ,str ):#line:1069
        OO0O0OOO0OO0OOO0O =pd .concat ([O000O0O0OOO0OOOO0 [-1 ][O00O0OO0OOOOOO0OO ],O000O0O0OOO0OOOO0 [-1 ][OOOO0O0O0O0OOOO00 ],OOO00OO0O0O00O0O0 ],axis =1 ,join ="outer")#line:1070
        O0000O0000O0000O0 =OO0O0OOO0OO0OOO0O .apply (OOO0O0O000OOO0O0O ,axis =1 )#line:1071
        O0000O0000O0000O0 =pd .DataFrame (O0000O0000O0000O0 )#line:1072
        O0000O0000O0000O0 .columns =[O00O000O0O0O00O0O ]#line:1073
    elif isinstance (O00O0OO0OOOOOO0OO ,str ):#line:1074
        O0000O0OOOO0O00O0 =pd .Series ([OOOO0O0O0O0OOOO00 ]*len (O000O0O0OOO0OOOO0 [-1 ]),index =O000O0O0OOO0OOOO0 [-1 ].index )#line:1075
        OO0O0OOO0OO0OOO0O =pd .concat ([O000O0O0OOO0OOOO0 [-1 ][O00O0OO0OOOOOO0OO ],O0000O0OOOO0O00O0 ,OOO00OO0O0O00O0O0 ],axis =1 ,join ="outer")#line:1076
        O0000O0000O0000O0 =OO0O0OOO0OO0OOO0O .apply (OOO0O0O000OOO0O0O ,axis =1 )#line:1077
        O0000O0000O0000O0 =pd .DataFrame (O0000O0000O0000O0 )#line:1078
        O0000O0000O0000O0 .columns =[O00O000O0O0O00O0O ]#line:1079
    elif isinstance (OOOO0O0O0O0OOOO00 ,str ):#line:1080
        O0000O0OOOO0O00O0 =pd .Series ([O00O0OO0OOOOOO0OO ]*len (O000O0O0OOO0OOOO0 [-1 ]),index =O000O0O0OOO0OOOO0 [-1 ].index )#line:1081
        OO0O0OOO0OO0OOO0O =pd .concat ([O0000O0OOOO0O00O0 ,O000O0O0OOO0OOOO0 [-1 ][OOOO0O0O0O0OOOO00 ],OOO00OO0O0O00O0O0 ],axis =1 ,join ="outer")#line:1082
        O0000O0000O0000O0 =OO0O0OOO0OO0OOO0O .apply (OOO0O0O000OOO0O0O ,axis =1 )#line:1083
        O0000O0000O0000O0 =pd .DataFrame (O0000O0000O0000O0 )#line:1084
        O0000O0000O0000O0 .columns =[O00O000O0O0O00O0O ]#line:1085
    else :#line:1086
        O00O0O0000OO0O000 =pd .Series ([O00O0OO0OOOOOO0OO ]*len (O000O0O0OOO0OOOO0 [-1 ]),index =O000O0O0OOO0OOOO0 [-1 ].index )#line:1087
        OO0OO0O00000O0O00 =pd .Series ([OOOO0O0O0O0OOOO00 ]*len (O000O0O0OOO0OOOO0 [-1 ]),index =O000O0O0OOO0OOOO0 [-1 ].index )#line:1088
        OO0O0OOO0OO0OOO0O =pd .concat ([O00O0O0000OO0O000 ,OO0OO0O00000O0O00 ,OOO00OO0O0O00O0O0 ],axis =1 ,join ="outer")#line:1089
        O0000O0000O0000O0 =OO0O0OOO0OO0OOO0O .apply (OOO0O0O000OOO0O0O ,axis =1 )#line:1090
        O0000O0000O0000O0 =pd .DataFrame (O0000O0000O0000O0 )#line:1091
        O0000O0000O0000O0 .columns =[O00O000O0O0O00O0O ]#line:1092
    O000O0O0OOO0OOOO0 [-1 ]=pd .concat ([O000O0O0OOO0OOOO0 [-1 ],O0000O0000O0000O0 ],axis =1 ,join ='outer')#line:1093
    gl .set_value ('listed',O000O0O0OOO0OOOO0 )#line:1094
    return O00O000O0O0O00O0O #line:1095
def lessthan (OOO000O0OO0O00000 ,OOOOO00O00OOOOO00 ):#line:1098
    O00OOOO0O00OO00O0 ="lessthan("+str (OOO000O0OO0O00000 )+","+str (OOOOO00O00OOOOO00 )+")"#line:1099
    O000OO0O00O0OO00O =gl .get_value ('listed')#line:1100
    if check_dup (O00OOOO0O00OO00O0 ):#line:1101
        return O00OOOO0O00OO00O0 #line:1102
    if isinstance (OOO000O0OO0O00000 ,str )and isinstance (OOOOO00O00OOOOO00 ,str ):#line:1103
        OO0000000O0OOO0O0 =pd .DataFrame (O000OO0O00O0OO00O [-1 ][[OOO000O0OO0O00000 ,OOOOO00O00OOOOO00 ]])#line:1104
        OO0000000O0OOO0O0 .columns =[['c1','c2']]#line:1105
        OO0000000O0OOO0O0 =OO0000000O0OOO0O0 .dropna (axis =0 ,how ='any')#line:1106
        O0OO0O0O0O0OO000O =pd .DataFrame (OO0000000O0OOO0O0 ['c1']<OO0000000O0OOO0O0 ['c2'])#line:1107
        O0OO0O0O0O0OO000O .columns =[O00OOOO0O00OO00O0 ]#line:1108
    elif isinstance (OOO000O0OO0O00000 ,str ):#line:1109
        OO0000000O0OOO0O0 =pd .DataFrame (O000OO0O00O0OO00O [-1 ][OOO000O0OO0O00000 ])#line:1110
        OO0000000O0OOO0O0 .columns =['c1']#line:1111
        OO0000000O0OOO0O0 =OO0000000O0OOO0O0 .dropna (axis =0 ,how ='any')#line:1112
        O0OO0O0O0O0OO000O =pd .DataFrame (OO0000000O0OOO0O0 ['c1']<OOOOO00O00OOOOO00 )#line:1113
        O0OO0O0O0O0OO000O .index =OO0000000O0OOO0O0 .index #line:1114
        O0OO0O0O0O0OO000O .columns =[O00OOOO0O00OO00O0 ]#line:1115
    elif isinstance (OOOOO00O00OOOOO00 ,str ):#line:1116
        OO0000000O0OOO0O0 =pd .DataFrame (O000OO0O00O0OO00O [-1 ][OOOOO00O00OOOOO00 ])#line:1117
        OO0000000O0OOO0O0 .columns =['c2']#line:1118
        OO0000000O0OOO0O0 =OO0000000O0OOO0O0 .dropna (axis =0 ,how ='any')#line:1119
        O0OO0O0O0O0OO000O =pd .DataFrame (OOO000O0OO0O00000 <OO0000000O0OOO0O0 ['c2'])#line:1120
        O0OO0O0O0O0OO000O .index =OO0000000O0OOO0O0 .index #line:1121
        O0OO0O0O0O0OO000O .columns =[O00OOOO0O00OO00O0 ]#line:1122
    else :#line:1123
        O0OO0O0O0O0OO000O =pd .DataFrame (OOO000O0OO0O00000 <OOOOO00O00OOOOO00 ,index =O000OO0O00O0OO00O [-1 ].index ,columns =[O00OOOO0O00OO00O0 ])#line:1124
    O000OO0O00O0OO00O [-1 ]=pd .concat ([O000OO0O00O0OO00O [-1 ],O0OO0O0O0O0OO000O ],axis =1 ,join ='outer')#line:1125
    gl .set_value ('listed',O000OO0O00O0OO00O )#line:1126
    return O00OOOO0O00OO00O0 #line:1127
def lessorequal (OO0O0O0O0OO0O0O0O ,OO0OO0O00O000O000 ):#line:1130
    OOO0O0OOOOO0O0OOO ="lessorequal("+str (OO0O0O0O0OO0O0O0O )+","+str (OO0OO0O00O000O000 )+")"#line:1131
    OO00O0O0O00OO0OO0 =gl .get_value ('listed')#line:1132
    if check_dup (OOO0O0OOOOO0O0OOO ):#line:1133
        return OOO0O0OOOOO0O0OOO #line:1134
    if isinstance (OO0O0O0O0OO0O0O0O ,str )and isinstance (OO0OO0O00O000O000 ,str ):#line:1135
        O0000000O0O00OOOO =pd .DataFrame (OO00O0O0O00OO0OO0 [-1 ][[OO0O0O0O0OO0O0O0O ,OO0OO0O00O000O000 ]])#line:1136
        O0000000O0O00OOOO .columns =[['c1','c2']]#line:1137
        O0000000O0O00OOOO =O0000000O0O00OOOO .dropna (axis =0 ,how ='any')#line:1138
        OO0OOOOO00O0O0O00 =pd .DataFrame (O0000000O0O00OOOO ['c1']<=O0000000O0O00OOOO ['c2'])#line:1139
        OO0OOOOO00O0O0O00 .columns =[OOO0O0OOOOO0O0OOO ]#line:1140
    elif isinstance (OO0O0O0O0OO0O0O0O ,str ):#line:1141
        O0000000O0O00OOOO =pd .DataFrame (OO00O0O0O00OO0OO0 [-1 ][OO0O0O0O0OO0O0O0O ])#line:1142
        O0000000O0O00OOOO .columns =['c1']#line:1143
        O0000000O0O00OOOO =O0000000O0O00OOOO .dropna (axis =0 ,how ='any')#line:1144
        OO0OOOOO00O0O0O00 =pd .DataFrame (O0000000O0O00OOOO ['c1']<=OO0OO0O00O000O000 )#line:1145
        OO0OOOOO00O0O0O00 .index =O0000000O0O00OOOO .index #line:1146
        OO0OOOOO00O0O0O00 .columns =[OOO0O0OOOOO0O0OOO ]#line:1147
    elif isinstance (OO0OO0O00O000O000 ,str ):#line:1148
        O0000000O0O00OOOO =pd .DataFrame (OO00O0O0O00OO0OO0 [-1 ][OO0OO0O00O000O000 ])#line:1149
        O0000000O0O00OOOO .columns =['c2']#line:1150
        O0000000O0O00OOOO =O0000000O0O00OOOO .dropna (axis =0 ,how ='any')#line:1151
        OO0OOOOO00O0O0O00 =pd .DataFrame (OO0O0O0O0OO0O0O0O <=O0000000O0O00OOOO ['c2'])#line:1152
        OO0OOOOO00O0O0O00 .index =O0000000O0O00OOOO .index #line:1153
        OO0OOOOO00O0O0O00 .columns =[OOO0O0OOOOO0O0OOO ]#line:1154
    else :#line:1155
        OO0OOOOO00O0O0O00 =pd .DataFrame (OO0O0O0O0OO0O0O0O <=OO0OO0O00O000O000 ,index =OO00O0O0O00OO0OO0 [-1 ].index ,columns =[OOO0O0OOOOO0O0OOO ])#line:1156
    OO00O0O0O00OO0OO0 [-1 ]=pd .concat ([OO00O0O0O00OO0OO0 [-1 ],OO0OOOOO00O0O0O00 ],axis =1 ,join ='outer')#line:1157
    gl .set_value ('listed',OO00O0O0O00OO0OO0 )#line:1158
    return OOO0O0OOOOO0O0OOO #line:1159
def greaterthan (O00OOOOO0000OOO00 ,OO000OO0OOOO0OO0O ):#line:1162
    OO0OOO0OOO000000O ="greaterthan("+str (O00OOOOO0000OOO00 )+","+str (OO000OO0OOOO0OO0O )+")"#line:1163
    OO00O0OOO00O0OO0O =gl .get_value ('listed')#line:1164
    if check_dup (OO0OOO0OOO000000O ):#line:1165
        return OO0OOO0OOO000000O #line:1166
    if isinstance (O00OOOOO0000OOO00 ,str )and isinstance (OO000OO0OOOO0OO0O ,str ):#line:1167
        O0OO00O0OOOO0O0O0 =pd .DataFrame (OO00O0OOO00O0OO0O [-1 ][[O00OOOOO0000OOO00 ,OO000OO0OOOO0OO0O ]])#line:1168
        O0OO00O0OOOO0O0O0 .columns =[['c1','c2']]#line:1169
        O0OO00O0OOOO0O0O0 =O0OO00O0OOOO0O0O0 .dropna (axis =0 ,how ='any')#line:1170
        O000OOO000O0O0O00 =pd .DataFrame (O0OO00O0OOOO0O0O0 ['c1']>O0OO00O0OOOO0O0O0 ['c2'])#line:1171
        O000OOO000O0O0O00 .columns =[OO0OOO0OOO000000O ]#line:1172
    elif isinstance (O00OOOOO0000OOO00 ,str ):#line:1173
        O0OO00O0OOOO0O0O0 =pd .DataFrame (OO00O0OOO00O0OO0O [-1 ][O00OOOOO0000OOO00 ])#line:1174
        O0OO00O0OOOO0O0O0 .columns =['c1']#line:1175
        O0OO00O0OOOO0O0O0 =O0OO00O0OOOO0O0O0 .dropna (axis =0 ,how ='any')#line:1176
        O000OOO000O0O0O00 =pd .DataFrame (O0OO00O0OOOO0O0O0 ['c1']>OO000OO0OOOO0OO0O )#line:1177
        O000OOO000O0O0O00 .index =O0OO00O0OOOO0O0O0 .index #line:1178
        O000OOO000O0O0O00 .columns =[OO0OOO0OOO000000O ]#line:1179
    elif isinstance (OO000OO0OOOO0OO0O ,str ):#line:1180
        O0OO00O0OOOO0O0O0 =pd .DataFrame (OO00O0OOO00O0OO0O [-1 ][OO000OO0OOOO0OO0O ])#line:1181
        O0OO00O0OOOO0O0O0 .columns =['c2']#line:1182
        O0OO00O0OOOO0O0O0 =O0OO00O0OOOO0O0O0 .dropna (axis =0 ,how ='any')#line:1183
        O000OOO000O0O0O00 =pd .DataFrame (O00OOOOO0000OOO00 >O0OO00O0OOOO0O0O0 ['c2'])#line:1184
        O000OOO000O0O0O00 .index =O0OO00O0OOOO0O0O0 .index #line:1185
        O000OOO000O0O0O00 .columns =[OO0OOO0OOO000000O ]#line:1186
    else :#line:1187
        O000OOO000O0O0O00 =pd .DataFrame (O00OOOOO0000OOO00 >OO000OO0OOOO0OO0O ,index =OO00O0OOO00O0OO0O [-1 ].index ,columns =[OO0OOO0OOO000000O ])#line:1188
    OO00O0OOO00O0OO0O [-1 ]=pd .concat ([OO00O0OOO00O0OO0O [-1 ],O000OOO000O0O0O00 ],axis =1 ,join ='outer')#line:1189
    gl .set_value ('listed',OO00O0OOO00O0OO0O )#line:1190
    return OO0OOO0OOO000000O #line:1191
def greaterorequal (OO00OOO0O00O0O000 ,O00O0OOO000OOOOOO ):#line:1194
    OOO000000O0O0O00O ="greaterorequal("+str (OO00OOO0O00O0O000 )+","+str (O00O0OOO000OOOOOO )+")"#line:1195
    O00O00000OOOOOOOO =gl .get_value ('listed')#line:1196
    if check_dup (OOO000000O0O0O00O ):#line:1197
        return OOO000000O0O0O00O #line:1198
    if isinstance (OO00OOO0O00O0O000 ,str )and isinstance (O00O0OOO000OOOOOO ,str ):#line:1199
        O00O0OOO00000000O =pd .DataFrame (O00O00000OOOOOOOO [-1 ][[OO00OOO0O00O0O000 ,O00O0OOO000OOOOOO ]])#line:1200
        O00O0OOO00000000O .columns =[['c1','c2']]#line:1201
        O00O0OOO00000000O =O00O0OOO00000000O .dropna (axis =0 ,how ='any')#line:1202
        OOO000OOOOO0O0OOO =pd .DataFrame (O00O0OOO00000000O ['c1']>=O00O0OOO00000000O ['c2'])#line:1203
        OOO000OOOOO0O0OOO .columns =[OOO000000O0O0O00O ]#line:1204
    elif isinstance (OO00OOO0O00O0O000 ,str ):#line:1205
        O00O0OOO00000000O =pd .DataFrame (O00O00000OOOOOOOO [-1 ][OO00OOO0O00O0O000 ])#line:1206
        O00O0OOO00000000O .columns =['c1']#line:1207
        O00O0OOO00000000O =O00O0OOO00000000O .dropna (axis =0 ,how ='any')#line:1208
        OOO000OOOOO0O0OOO =pd .DataFrame (O00O0OOO00000000O ['c1']>=O00O0OOO000OOOOOO )#line:1209
        OOO000OOOOO0O0OOO .index =O00O0OOO00000000O .index #line:1210
        OOO000OOOOO0O0OOO .columns =[OOO000000O0O0O00O ]#line:1211
    elif isinstance (O00O0OOO000OOOOOO ,str ):#line:1212
        O00O0OOO00000000O =pd .DataFrame (O00O00000OOOOOOOO [-1 ][O00O0OOO000OOOOOO ])#line:1213
        O00O0OOO00000000O .columns =['c2']#line:1214
        O00O0OOO00000000O =O00O0OOO00000000O .dropna (axis =0 ,how ='any')#line:1215
        OOO000OOOOO0O0OOO =pd .DataFrame (OO00OOO0O00O0O000 >=O00O0OOO00000000O ['c2'])#line:1216
        OOO000OOOOO0O0OOO .index =O00O0OOO00000000O .index #line:1217
        OOO000OOOOO0O0OOO .columns =[OOO000000O0O0O00O ]#line:1218
    else :#line:1219
        OOO000OOOOO0O0OOO =pd .DataFrame (OO00OOO0O00O0O000 >=O00O0OOO000OOOOOO ,index =O00O00000OOOOOOOO [-1 ].index ,columns =[OOO000000O0O0O00O ])#line:1220
    O00O00000OOOOOOOO [-1 ]=pd .concat ([O00O00000OOOOOOOO [-1 ],OOO000OOOOO0O0OOO ],axis =1 ,join ='outer')#line:1221
    gl .set_value ('listed',O00O00000OOOOOOOO )#line:1222
    return OOO000000O0O0O00O #line:1223
def equal (O00O00O0OOO000O00 ,O0OO0O000O0O0O0O0 ):#line:1226
    OOO00000OO0O00O0O ="equal("+str (O00O00O0OOO000O00 )+","+str (O0OO0O000O0O0O0O0 )+")"#line:1227
    OOO0OOOOOO0O000O0 =gl .get_value ('listed')#line:1228
    if check_dup (OOO00000OO0O00O0O ):#line:1229
        return OOO00000OO0O00O0O #line:1230
    if isinstance (O00O00O0OOO000O00 ,str )and isinstance (O0OO0O000O0O0O0O0 ,str ):#line:1231
        OOO0O0O0O00OOO000 =pd .DataFrame (OOO0OOOOOO0O000O0 [-1 ][[O00O00O0OOO000O00 ,O0OO0O000O0O0O0O0 ]])#line:1232
        OOO0O0O0O00OOO000 .columns =[['c1','c2']]#line:1233
        OOO0O0O0O00OOO000 =OOO0O0O0O00OOO000 .dropna (axis =0 ,how ='any')#line:1234
        O0OOO0OOO0OOO00O0 =pd .DataFrame (OOO0O0O0O00OOO000 ['c1']==OOO0O0O0O00OOO000 ['c2'])#line:1235
        O0OOO0OOO0OOO00O0 .columns =[OOO00000OO0O00O0O ]#line:1236
    elif isinstance (O00O00O0OOO000O00 ,str ):#line:1237
        OOO0O0O0O00OOO000 =pd .DataFrame (OOO0OOOOOO0O000O0 [-1 ][O00O00O0OOO000O00 ])#line:1238
        OOO0O0O0O00OOO000 .columns =['c1']#line:1239
        OOO0O0O0O00OOO000 =OOO0O0O0O00OOO000 .dropna (axis =0 ,how ='any')#line:1240
        O0OOO0OOO0OOO00O0 =pd .DataFrame (OOO0O0O0O00OOO000 ['c1']==O0OO0O000O0O0O0O0 )#line:1241
        O0OOO0OOO0OOO00O0 .index =OOO0O0O0O00OOO000 .index #line:1242
        O0OOO0OOO0OOO00O0 .columns =[OOO00000OO0O00O0O ]#line:1243
    elif isinstance (O0OO0O000O0O0O0O0 ,str ):#line:1244
        OOO0O0O0O00OOO000 =pd .DataFrame (OOO0OOOOOO0O000O0 [-1 ][O0OO0O000O0O0O0O0 ])#line:1245
        OOO0O0O0O00OOO000 .columns =['c2']#line:1246
        OOO0O0O0O00OOO000 =OOO0O0O0O00OOO000 .dropna (axis =0 ,how ='any')#line:1247
        O0OOO0OOO0OOO00O0 =pd .DataFrame (O00O00O0OOO000O00 ==OOO0O0O0O00OOO000 ['c2'])#line:1248
        O0OOO0OOO0OOO00O0 .index =OOO0O0O0O00OOO000 .index #line:1249
        O0OOO0OOO0OOO00O0 .columns =[OOO00000OO0O00O0O ]#line:1250
    else :#line:1251
        O0OOO0OOO0OOO00O0 =pd .DataFrame (O00O00O0OOO000O00 ==O0OO0O000O0O0O0O0 ,index =OOO0OOOOOO0O000O0 [-1 ].index ,columns =[OOO00000OO0O00O0O ])#line:1252
    OOO0OOOOOO0O000O0 [-1 ]=pd .concat ([OOO0OOOOOO0O000O0 [-1 ],O0OOO0OOO0OOO00O0 ],axis =1 ,join ='outer')#line:1253
    gl .set_value ('listed',OOO0OOOOOO0O000O0 )#line:1254
    return OOO00000OO0O00O0O #line:1255
def notequal (OOO00000O0OO0000O ,OOO0OO00OO0O00OO0 ):#line:1258
    O0OO0OO0O00OO0OOO ="notequal("+str (OOO00000O0OO0000O )+","+str (OOO0OO00OO0O00OO0 )+")"#line:1259
    OO000O00000OO0OOO =gl .get_value ('listed')#line:1260
    if check_dup (O0OO0OO0O00OO0OOO ):#line:1261
        return O0OO0OO0O00OO0OOO #line:1262
    if isinstance (OOO00000O0OO0000O ,str )and isinstance (OOO0OO00OO0O00OO0 ,str ):#line:1263
        O0OOOOO0O000OO000 =pd .DataFrame (OO000O00000OO0OOO [-1 ][[OOO00000O0OO0000O ,OOO0OO00OO0O00OO0 ]])#line:1264
        O0OOOOO0O000OO000 .columns =[['c1','c2']]#line:1265
        O0OOOOO0O000OO000 =O0OOOOO0O000OO000 .dropna (axis =0 ,how ='any')#line:1266
        O0OO0000O0OO0OOO0 =pd .DataFrame (O0OOOOO0O000OO000 ['c1']!=O0OOOOO0O000OO000 ['c2'])#line:1267
        O0OO0000O0OO0OOO0 .columns =[O0OO0OO0O00OO0OOO ]#line:1268
    elif isinstance (OOO00000O0OO0000O ,str ):#line:1269
        O0OOOOO0O000OO000 =pd .DataFrame (OO000O00000OO0OOO [-1 ][OOO00000O0OO0000O ])#line:1270
        O0OOOOO0O000OO000 .columns =['c1']#line:1271
        O0OOOOO0O000OO000 =O0OOOOO0O000OO000 .dropna (axis =0 ,how ='any')#line:1272
        O0OO0000O0OO0OOO0 =pd .DataFrame (O0OOOOO0O000OO000 ['c1']!=OOO0OO00OO0O00OO0 )#line:1273
        O0OO0000O0OO0OOO0 .index =O0OOOOO0O000OO000 .index #line:1274
        O0OO0000O0OO0OOO0 .columns =[O0OO0OO0O00OO0OOO ]#line:1275
    elif isinstance (OOO0OO00OO0O00OO0 ,str ):#line:1276
        O0OOOOO0O000OO000 =pd .DataFrame (OO000O00000OO0OOO [-1 ][OOO0OO00OO0O00OO0 ])#line:1277
        O0OOOOO0O000OO000 .columns =['c2']#line:1278
        O0OOOOO0O000OO000 =O0OOOOO0O000OO000 .dropna (axis =0 ,how ='any')#line:1279
        O0OO0000O0OO0OOO0 =pd .DataFrame (OOO00000O0OO0000O !=O0OOOOO0O000OO000 ['c2'])#line:1280
        O0OO0000O0OO0OOO0 .index =O0OOOOO0O000OO000 .index #line:1281
        O0OO0000O0OO0OOO0 .columns =[O0OO0OO0O00OO0OOO ]#line:1282
    else :#line:1283
        O0OO0000O0OO0OOO0 =pd .DataFrame (OOO00000O0OO0000O !=OOO0OO00OO0O00OO0 ,index =OO000O00000OO0OOO [-1 ].index ,columns =[O0OO0OO0O00OO0OOO ])#line:1284
    OO000O00000OO0OOO [-1 ]=pd .concat ([OO000O00000OO0OOO [-1 ],O0OO0000O0OO0OOO0 ],axis =1 ,join ='outer')#line:1285
    gl .set_value ('listed',OO000O00000OO0OOO )#line:1286
    return O0OO0OO0O00OO0OOO #line:1287
def also (OOOOOO00O0O00OO0O ,O0O00OOOOOOOO000O ):#line:1290
    O000O000O00OO0OOO ="also("+OOOOOO00O0O00OO0O +","+O0O00OOOOOOOO000O +")"#line:1291
    O0OOO00000000OO00 =gl .get_value ('listed')#line:1292
    if check_dup (O000O000O00OO0OOO ):#line:1293
        return O000O000O00OO0OOO #line:1294
    O0OO0OO00O000OO0O =pd .DataFrame (O0OOO00000000OO00 [-1 ][[OOOOOO00O0O00OO0O ,O0O00OOOOOOOO000O ]])#line:1295
    O0OO0OO00O000OO0O .columns =[['c1','c2']]#line:1296
    O0O00O00000OOOO0O =pd .DataFrame (O0OO0OO00O000OO0O ['c1']&O0OO0OO00O000OO0O ['c2'],index =O0OO0OO00O000OO0O .index )#line:1297
    O0O00O00000OOOO0O .columns =[O000O000O00OO0OOO ]#line:1298
    O0OOO00000000OO00 [-1 ]=pd .concat ([O0OOO00000000OO00 [-1 ],O0O00O00000OOOO0O ],axis =1 ,join ='outer')#line:1299
    gl .set_value ('listed',O0OOO00000000OO00 )#line:1300
    return O000O000O00OO0OOO #line:1301
def oror (O0OO0O00O00O00O00 ,O0000O0OO000O0O0O ):#line:1304
    OOO0OOO000O0OO000 ="oror("+O0OO0O00O00O00O00 +","+O0000O0OO000O0O0O +")"#line:1305
    O000OO0OOO0O0OOO0 =gl .get_value ('listed')#line:1306
    if check_dup (OOO0OOO000O0OO000 ):#line:1307
        return OOO0OOO000O0OO000 #line:1308
    OOOOOOOO0OO000OO0 =pd .DataFrame (O000OO0OOO0O0OOO0 [-1 ][[O0OO0O00O00O00O00 ,O0000O0OO000O0O0O ]])#line:1309
    OOOOOOOO0OO000OO0 .columns =[['c1','c2']]#line:1310
    O0OOOO0OO0000O00O =pd .DataFrame (OOOOOOOO0OO000OO0 ['c1']|OOOOOOOO0OO000OO0 ['c2'],index =OOOOOOOO0OO000OO0 .index )#line:1311
    O0OOOO0OO0000O00O .columns =[OOO0OOO000O0OO000 ]#line:1312
    O000OO0OOO0O0OOO0 [-1 ]=pd .concat ([O000OO0OOO0O0OOO0 [-1 ],O0OOOO0OO0000O00O ],axis =1 ,join ='outer')#line:1313
    gl .set_value ('listed',O000OO0OOO0O0OOO0 )#line:1314
    return OOO0OOO000O0OO000 #line:1315
def negative (O0O00O0OOO000OO0O ):#line:1318
    O0O00000OOO0OOOO0 ="negative("+O0O00O0OOO000OO0O +")"#line:1319
    OOO000O0000OOOO0O =gl .get_value ('listed')#line:1320
    if check_dup (O0O00000OOO0OOOO0 ):#line:1321
        return O0O00000OOO0OOOO0 #line:1322
    O000O0O00OOOOOO00 =pd .DataFrame (OOO000O0000OOOO0O [-1 ][[O0O00O0OOO000OO0O ]])#line:1323
    O000O0O00OOOOOO00 .columns =[['c1']]#line:1324
    OOO0O0OO0O000OOO0 =pd .DataFrame (O000O0O00OOOOOO00 ['c1']!=True ,index =O000O0O00OOOOOO00 .index )#line:1325
    OOO0O0OO0O000OOO0 .columns =[O0O00000OOO0OOOO0 ]#line:1326
    OOO000O0000OOOO0O [-1 ]=pd .concat ([OOO000O0000OOOO0O [-1 ],OOO0O0OO0O000OOO0 ],axis =1 ,join ='outer')#line:1327
    gl .set_value ('listed',OOO000O0000OOOO0O )#line:1328
    return O0O00000OOO0OOOO0 #line:1329
