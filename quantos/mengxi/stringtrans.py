# _*_ coding:utf-8 _*_
import numpy as np #line:2
import pandas as pd #line:3
import re #line:4
def repair (OO00OOO0000OOO0OO ):#line:6
    O00O000OO0OOO0O0O =OO00OOO0000OOO0OO .lower ()#line:7
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('highday','argmax')#line:8
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('lowday','argmin')#line:9
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('adv(','mean(volume,')#line:10
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('returns','returns()')#line:11
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('close','close()')#line:12
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('open','opened()')#line:13
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('high','high()')#line:14
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('low','low()')#line:15
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('volume','volume()')#line:16
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('money','money()')#line:17
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('avg','avg()')#line:18
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('sum','summation')#line:19
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('max','maximum')#line:20
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('min','minimum')#line:21
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('mean','tsmean')#line:22
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('coviance','cov')#line:23
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('prod','product')#line:24
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('exp','exponential')#line:25
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('log','logarithm')#line:26
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('abs','absolute')#line:27
    O00O000OO0OOO0O0O =O00O000OO0OOO0O0O .replace ('count','counttt')#line:28
    return O00O000OO0OOO0O0O #line:30
SUPPORT_SIGN ={'[':99 ,'^':50 ,'*':30 ,'%':30 ,'/':30 ,'-':20 ,'+':20 ,'>':10 ,'<':10 ,'>=':10 ,'<=':10 ,'==':5 ,'!=':5 ,'&&':3 ,'||':3 }#line:33
first_sign =['!','&','=','>','<','|']#line:35
NUMBER_PATTERN =re .compile ('[!a-zA-Z0-9.]')#line:37
ignore_list =[' ','_']#line:38
def check (O0O000O0O00OOO0O0 ):#line:41
    O000O0000O0O0O00O =Stack ()#line:42
    O00O0OOOOOO0O0OO0 =Stack ()#line:43
    for O0OO0OO00O0O0O0OO in O0O000O0O00OOO0O0 :#line:44
        if O0OO0OO00O0O0O0OO =='(':#line:45
            O000O0000O0O0O00O .push ('(')#line:46
        elif O0OO0OO00O0O0O0OO ==')':#line:47
            if O000O0000O0O0O00O .peek ()!='(':#line:48
                raise TypeError #line:49
            else :#line:50
                O000O0000O0O0O00O .pop ()#line:51
        elif O0OO0OO00O0O0O0OO =='[':#line:52
            O00O0OOOOOO0O0OO0 .push ('[')#line:53
        elif O0OO0OO00O0O0O0OO ==']':#line:54
            if O00O0OOOOOO0O0OO0 .peek ()!='[':#line:55
                raise TypeError #line:56
            else :#line:57
                O00O0OOOOOO0O0OO0 .pop ()#line:58
    if not O000O0000O0O0O00O .empty ()or not O00O0OOOOOO0O0OO0 .empty ():#line:59
        print ("括号输入有误")#line:60
        raise TypeError #line:61
def init (OOOO0OOOO000O0O00 ):#line:63
    check (OOOO0OOOO000O0O00 )#line:64
    OOOO0OOOO000O0O00 =OOOO0OOOO000O0O00 .replace ('pi','3.14159')#line:65
    for OOO00OO000O0OO0O0 in ignore_list :#line:66
        OOOO0OOOO000O0O00 =OOOO0OOOO000O0O00 .replace (OOO00OO000O0OO0O0 ,'')#line:67
    return OOOO0OOOO000O0O00 #line:68
def body (OOOO000O0OOO0O0OO ):#line:71
    OOOO000O0OOO0O0OO =init (OOOO000O0OOO0O0OO )#line:72
    OOOO000O0OOO0O0OO =chang_allcondition (OOOO000O0OOO0O0OO )#line:73
    OOOO000O0OOO0O0OO =to_suffix (OOOO000O0OOO0O0OO )#line:74
    return text_neg (OOOO000O0OOO0O0OO )#line:75
def to_suffix (OO0OOOOOOOOOOO0OO ):#line:78
    O000OO00OO00O0O00 =Stack ()#line:80
    OOOO00OOO00OOOO0O =[]#line:81
    OOO000O0O0OOO00OO =None #line:82
    OO000O0O0O0000000 =0 #line:83
    OOOOOOOO0OOOO0000 =0 #line:84
    OO00O0OO000OO00O0 =0 #line:85
    if not isinstance (OO0OOOOOOOOOOO0OO ,str ):#line:87
        raise TypeError #line:88
    if search_point (OO0OOOOOOOOOOO0OO )==0 :#line:89
        for OOO00OOOO0O0OO0OO in OO0OOOOOOOOOOO0OO :#line:90
            if not OO00O0OO000OO00O0 :#line:91
                if OO000O0O0O0000000 :#line:92
                    OOOO00OOO00OOOO0O [-1 ]+=OOO00OOOO0O0OO0OO #line:93
                    if OOO00OOOO0O0OO0OO =='(':#line:94
                        OO000O0O0O0000000 +=1 #line:95
                    if OOO00OOOO0O0OO0OO ==')':#line:96
                        OO000O0O0O0000000 -=1 #line:97
                        if OO000O0O0O0000000 ==0 :#line:98
                            O0O0OO0OO0O0OO000 =extract (OOOO00OOO00OOOO0O [-1 ])#line:99
                            OOOO00OOO00OOOO0O [-1 ]=O0O0OO0OO0O0OO000 [0 ]+'('+to_suffix (O0O0OO0OO0O0OO000 [1 ])+')'#line:100
                    OOOOOOOO0OOOO0000 +=1 #line:102
                    continue #line:103
                if OOO00OOOO0O0OO0OO in first_sign :#line:104
                    if text_double (OO0OOOOOOOOOOO0OO ,OOOOOOOO0OOOO0000 ):#line:105
                        OOO00OOOO0O0OO0OO =OOO00OOOO0O0OO0OO +OO0OOOOOOOOOOO0OO [OOOOOOOO0OOOO0000 +1 ]#line:106
                        OO00O0OO000OO00O0 =1 #line:107
                if OOO00OOOO0O0OO0OO in SUPPORT_SIGN :#line:109
                    O000000OOOO0OOO0O =O000OO00OO00O0O00 .peek ()#line:110
                    while O000000OOOO0OOO0O and SUPPORT_SIGN [OOO00OOOO0O0OO0OO ]<=SUPPORT_SIGN [O000000OOOO0OOO0O ]:#line:111
                        if O000000OOOO0OOO0O =='[':#line:112
                            break #line:113
                        OOOO00OOO00OOOO0O .append (O000OO00OO00O0O00 .pop ())#line:114
                        O000000OOOO0OOO0O =O000OO00OO00O0O00 .peek ()#line:115
                    O000OO00OO00O0O00 .push (OOO00OOOO0O0OO0OO )#line:116
                elif OOO00OOOO0O0OO0OO ==']':#line:117
                    O000000OOOO0OOO0O =O000OO00OO00O0O00 .peek ()#line:118
                    while O000000OOOO0OOO0O !='[':#line:119
                        O000000OOOO0OOO0O =O000OO00OO00O0O00 .pop ()#line:120
                        OOOO00OOO00OOOO0O .append (O000000OOOO0OOO0O )#line:121
                        O000000OOOO0OOO0O =O000OO00OO00O0O00 .peek ()#line:122
                    O000OO00OO00O0O00 .pop ()#line:123
                elif NUMBER_PATTERN .match (OOO00OOOO0O0OO0OO ):#line:124
                    if OOO000O0O0OOO00OO and NUMBER_PATTERN .match (OOO000O0O0OOO00OO ):#line:125
                        OOOO00OOO00OOOO0O [-1 ]+=OOO00OOOO0O0OO0OO #line:126
                    else :#line:127
                        OOOO00OOO00OOOO0O .append (OOO00OOOO0O0OO0OO )#line:128
                elif OOO00OOOO0O0OO0OO =='(':#line:129
                    if len (OOOO00OOO00OOOO0O )==0 :#line:130
                        OOOO00OOO00OOOO0O .append (OOO00OOOO0O0OO0OO )#line:131
                    else :#line:132
                        if NUMBER_PATTERN .match (OOO000O0O0OOO00OO ):#line:133
                            OOOO00OOO00OOOO0O [-1 ]+=OOO00OOOO0O0OO0OO #line:134
                        else :#line:135
                            OOOO00OOO00OOOO0O .append (OOO00OOOO0O0OO0OO )#line:136
                    OO000O0O0O0000000 =1 #line:137
                else :#line:138
                    print (OOO00OOOO0O0OO0OO )#line:139
                    raise TypeError #line:140
                OOO000O0O0OOO00OO =OOO00OOOO0O0OO0OO #line:141
                OOOOOOOO0OOOO0000 +=1 #line:142
            else :#line:143
                OO00O0OO000OO00O0 =0 #line:144
                OOO000O0O0OOO00OO =OO0OOOOOOOOOOO0OO [OOOOOOOO0OOOO0000 ]#line:145
                OOOOOOOO0OOOO0000 +=1 #line:146
        while not O000OO00OO00O0O00 .empty ():#line:147
            OOOO00OOO00OOOO0O .append (O000OO00OO00O0O00 .pop ())#line:148
        return text_neg (count (OOOO00OOO00OOOO0O ))#line:150
    else :#line:151
        OO0OOO0O0O00OOO00 =search_point (OO0OOOOOOOOOOO0OO )#line:152
        return to_suffix (OO0OOO0O0O00OOO00 [0 ])+','+to_suffix (OO0OOO0O0O00OOO00 [1 ])#line:153
def text_brackets (OO0OOOO0OOOO00O00 ):#line:155
    check (OO0OOOO0OOOO00O00 )#line:156
    if OO0OOOO0OOOO00O00 [0 ]!='('or OO0OOOO0OOOO00O00 [-1 ]!=')':#line:157
        return False #line:158
    else :#line:159
        OOOO0000OO0O000O0 =0 #line:160
        O000OO0O00OO00OOO =1 #line:161
        for OO0000O00O0OO00O0 in OO0OOOO0OOOO00O00 :#line:162
            if OO0000O00O0OO00O0 =='(':#line:163
                OOOO0000OO0O000O0 +=1 #line:164
            if OO0000O00O0OO00O0 ==')':#line:165
                OOOO0000OO0O000O0 -=1 #line:166
            if OOOO0000OO0O000O0 ==0 and O000OO0O00OO00OOO !=len (OO0OOOO0OOOO00O00 ):#line:167
                return False #line:168
            O000OO0O00OO00OOO +=1 #line:169
    return True #line:170
def count (O00OO00OOOO0000OO ):#line:173
    OO00000OO0OO0O00O =[]#line:174
    OO000O0O0O0OOO00O =len (O00OO00OOOO0000OO )#line:175
    for OO00O0O000O00OOOO in O00OO00OOOO0000OO :#line:176
        if OO00O0O000O00OOOO in list (SUPPORT_SIGN ):#line:177
            if OO00O0O000O00OOOO =="+":#line:178
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:179
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:180
                OO00000OO0OO0O00O .append ('plus'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:181
            elif OO00O0O000O00OOOO =="*":#line:182
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:183
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:184
                OO00000OO0OO0O00O .append ('multiply'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:185
            elif OO00O0O000O00OOOO =="%"or OO00O0O000O00OOOO =="/":#line:186
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:187
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:188
                OO00000OO0OO0O00O .append ('divide'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:189
            elif OO00O0O000O00OOOO =='^':#line:190
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:191
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:192
                OO00000OO0OO0O00O .append ('power'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:193
            elif OO00O0O000O00OOOO =='>=':#line:194
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:195
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:196
                OO00000OO0OO0O00O .append ('greaterorequal'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:197
            elif OO00O0O000O00OOOO =='<=':#line:198
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:199
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:200
                OO00000OO0OO0O00O .append ('lessorequal'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:201
            elif OO00O0O000O00OOOO =='<':#line:202
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:203
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:204
                OO00000OO0OO0O00O .append ('lessthan'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:205
            elif OO00O0O000O00OOOO =='>':#line:206
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:207
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:208
                OO00000OO0OO0O00O .append ('greaterthan'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:209
            elif OO00O0O000O00OOOO =='&&':#line:210
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:211
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:212
                OO00000OO0OO0O00O .append ('also'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:213
            elif OO00O0O000O00OOOO =='||':#line:214
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:215
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:216
                OO00000OO0OO0O00O .append ('oror'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:217
            elif OO00O0O000O00OOOO =='!=':#line:218
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:219
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:220
                OO00000OO0OO0O00O .append ('notequal'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:221
            elif OO00O0O000O00OOOO =='==':#line:222
                OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:223
                O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:224
                OO00000OO0OO0O00O .append ('equal'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:225
            elif OO00O0O000O00OOOO =="-":#line:226
                if len (OO00000OO0OO0O00O )>1 :#line:227
                    if len (OO00000OO0OO0O00O )==2 and OO000O0O0O0OOO00O ==2 :#line:228
                        OO00000OO0OO0O00O [-1 ]='-'+OO00000OO0OO0O00O [-1 ]#line:229
                        OO000O0O0O0OOO00O -=1 #line:230
                        continue #line:231
                    else :#line:232
                        OOOO000OO00O00000 =OO00000OO0OO0O00O .pop ()#line:233
                        O000000OO00OO00OO =OO00000OO0OO0O00O .pop ()#line:234
                        OO00000OO0OO0O00O .append ('subtract'+'('+O000000OO00OO00OO +','+OOOO000OO00O00000 +')')#line:235
                else :#line:236
                    OO00000OO0OO0O00O .append ('-'+OO00000OO0OO0O00O .pop ())#line:237
        else :#line:238
            if OO00O0O000O00OOOO [0 ]=='!':#line:239
                OO00O0O000O00OOOO ='negative'+'('+OO00O0O000O00OOOO [1 :]+')'#line:240
                OO00000OO0OO0O00O .append (OO00O0O000O00OOOO )#line:241
            elif text_brackets (OO00O0O000O00OOOO ):#line:242
                OO00000OO0OO0O00O .append (OO00O0O000O00OOOO [1 :len (OO00O0O000O00OOOO )-1 ])#line:243
            else :#line:244
                OO00000OO0OO0O00O .append (OO00O0O000O00OOOO )#line:245
        OO000O0O0O0OOO00O -=1 #line:246
    return ''.join (OO00000OO0OO0O00O )#line:247
def extract (O0O0O00O000OOO0O0 ):#line:250
    OO0O000O00O0OO0OO =O0O0O00O000OOO0O0 .find ("(")#line:251
    O00OO00OOO0O0OOOO =O0O0O00O000OOO0O0 .rfind (")")#line:252
    return [O0O0O00O000OOO0O0 [:OO0O000O00O0OO0OO ],O0O0O00O000OOO0O0 [OO0O000O00O0OO0OO +1 :O00OO00OOO0O0OOOO ]]#line:253
def search_point (O00OOO00OOOO0OOOO ):#line:256
    O0OO0O0OO00O000OO =0 #line:257
    O0000OO0O0O0OO00O =0 #line:258
    for OOOOOOO0OO0OOO0O0 in O00OOO00OOOO0OOOO :#line:259
        if OOOOOOO0OO0OOO0O0 =="(":#line:260
            O0OO0O0OO00O000OO +=1 #line:261
        if OOOOOOO0OO0OOO0O0 ==")":#line:262
            O0OO0O0OO00O000OO -=1 #line:263
        if OOOOOOO0OO0OOO0O0 ==','and O0OO0O0OO00O000OO ==0 :#line:264
            return [O00OOO00OOOO0OOOO [:O0000OO0O0O0OO00O ],O00OOO00OOOO0OOOO [O0000OO0O0O0OO00O +1 :]]#line:265
        O0000OO0O0O0OO00O +=1 #line:266
    return 0 #line:267
def text_double (O00OOO000O0O00O0O ,OO0OOO0O0OOOOO00O ):#line:270
    if (O00OOO000O0O00O0O [OO0OOO0O0OOOOO00O ]+O00OOO000O0O00O0O [OO0OOO0O0OOOOO00O +1 ])in list (SUPPORT_SIGN ):#line:271
        return 1 #line:272
    else :#line:273
        return 0 #line:274
def search (OO0OO00O00O000OO0 ,OO0OO0OO000OO0000 ):#line:277
    ""#line:283
    O000OOOOO00000000 =0 #line:284
    O0000000OOOOOOO0O =0 #line:285
    OO0O000O0OOO00O0O =OO0OO0OO000OO0000 -1 #line:286
    OOO0OO0000O0O00O0 =OO0OO0OO000OO0000 +1 #line:287
    OOOO0OO0O0OOOO0OO =OO0OO0OO000OO0000 +1 #line:288
    OOO000000OOOOO000 =0 #line:289
    for OO0O000O0OOO00O0O in range (OO0OO0OO000OO0000 -1 ,-1 ,-1 ):#line:290
        if OO0OO00O00O000OO0 [OO0O000O0OOO00O0O ]==']'or OO0OO00O00O000OO0 [OO0O000O0OOO00O0O ]==')':#line:291
            O000OOOOO00000000 +=1 #line:292
        elif OO0OO00O00O000OO0 [OO0O000O0OOO00O0O ]=='['or OO0OO00O00O000OO0 [OO0O000O0OOO00O0O ]=='(':#line:293
            O000OOOOO00000000 -=1 #line:294
        if O000OOOOO00000000 ==-1 :#line:295
            break #line:296
        if O000OOOOO00000000 ==0 and OO0OO00O00O000OO0 [OO0O000O0OOO00O0O ]==',':#line:297
            break #line:298
    for OOO0OO0000O0O00O0 in range (OO0OO0OO000OO0000 +1 ,len (OO0OO00O00O000OO0 )):#line:299
        if OO0OO00O00O000OO0 [OOO0OO0000O0O00O0 ]==']'or OO0OO00O00O000OO0 [OOO0OO0000O0O00O0 ]==')':#line:300
            O0000000OOOOOOO0O -=1 #line:301
        elif OO0OO00O00O000OO0 [OOO0OO0000O0O00O0 ]=='['or OO0OO00O00O000OO0 [OOO0OO0000O0O00O0 ]=='(':#line:302
            O0000000OOOOOOO0O +=1 #line:303
        if O0000000OOOOOOO0O ==-1 :#line:304
            break #line:305
        if O0000000OOOOOOO0O ==0 and OO0OO00O00O000OO0 [OOO0OO0000O0O00O0 ]==',':#line:306
            break #line:307
        if O0000000OOOOOOO0O ==0 and OO0OO00O00O000OO0 [OOO0OO0000O0O00O0 ]==':'and OOO000000OOOOO000 ==0 :#line:308
            OOOO0OO0O0OOOO0OO =OOO0OO0000O0O00O0 #line:309
            OOO000000OOOOO000 =1 #line:310
    if O000OOOOO00000000 ==0 and OO0O000O0OOO00O0O ==0 :#line:312
        OO0O000O0OOO00O0O =-1 #line:313
    if O0000000OOOOOOO0O ==0 and OOO0OO0000O0O00O0 ==len (OO0OO00O00O000OO0 )-1 :#line:314
        OOO0OO0000O0O00O0 =len (OO0OO00O00O000OO0 )#line:315
    return [OO0O000O0OOO00O0O ,OOOO0OO0O0OOOO0OO ,OOO0OO0000O0O00O0 ]#line:317
def chang_condition (O000O00O0000OOOO0 ):#line:320
    ""#line:326
    O0O0OO000OO0O000O =O000O00O0000OOOO0 .find ('?')#line:327
    O0OO00O0O0O000OOO =search (O000O00O0000OOOO0 ,O0O0OO000OO0O000O )#line:328
    O00000OO0OO000O0O =O000O00O0000OOOO0 [O0O0OO000OO0O000O +1 :O0OO00O0O0O000OOO [1 ]]#line:329
    O0OO0000OO0OOOO0O =O000O00O0000OOOO0 [O0OO00O0O0O000OOO [1 ]+1 :O0OO00O0O0O000OOO [2 ]]#line:330
    if O0OO00O0O0O000OOO [0 ]==-1 :#line:331
        O0O0O0OO00OOO0O00 =O000O00O0000OOOO0 [0 :O0O0OO000OO0O000O ]#line:332
        return 'condition('+body (O0O0O0OO00OOO0O00 )+','+body (O00000OO0OO000O0O )+','+body (O0OO0000OO0OOOO0O )+')'+O000O00O0000OOOO0 [O0OO00O0O0O000OOO [2 ]:]#line:334
    else :#line:335
        O0O0O0OO00OOO0O00 =O000O00O0000OOOO0 [O0OO00O0O0O000OOO [0 ]+1 :O0O0OO000OO0O000O ]#line:336
        return O000O00O0000OOOO0 [0 :O0OO00O0O0O000OOO [0 ]+1 ]+'condition('+body (O0O0O0OO00OOO0O00 )+','+body (O00000OO0OO000O0O )+','+body (O0OO0000OO0OOOO0O )+')'+O000O00O0000OOOO0 [O0OO00O0O0O000OOO [2 ]:]#line:338
def chang_allcondition (OOOO00O00OOO0O0OO ):#line:341
    ""#line:346
    while OOOO00O00OOO0O0OO .find ('?')!=-1 :#line:347
        OOOO00O00OOO0O0OO =chang_condition (OOOO00O00OOO0O0OO )#line:348
    return OOOO00O00OOO0O0OO #line:349
def text_neg (O0O00O0OOO000OOO0 ):#line:352
    if len (O0O00O0OOO000OOO0 )==0 :#line:353
        return O0O00O0OOO000OOO0 #line:354
    if O0O00O0OOO000OOO0 [0 ]=='-':#line:355
        return 'multiply'+'('+'-1'+','+O0O00O0OOO000OOO0 [1 :]+')'#line:356
    else :#line:357
        return O0O00O0OOO000OOO0 #line:358
class Stack (object ):#line:363
    def __init__ (O0O00OO0OOO00OO0O ):#line:364
        O0O00OO0OOO00OO0O .datas =[]#line:365
        O0O00OO0OOO00OO0O .length =0 #line:366
    def push (OOOOOOOO0O0O0O00O ,OO0OO0OOO0000O0OO ):#line:369
        OOOOOOOO0O0O0O00O .datas .append (OO0OO0OOO0000O0OO )#line:370
        OOOOOOOO0O0O0O00O .length +=1 #line:371
    def peek (O00OO000OO0O00O00 ):#line:373
        return None if O00OO000OO0O00O00 .empty ()else O00OO000OO0O00O00 .datas [len (O00OO000OO0O00O00 .datas )-1 ]#line:374
    def pop (OO00OOO00OOOO0OOO ):#line:376
        try :#line:377
            return OO00OOO00OOOO0OOO .peek ()#line:378
        finally :#line:379
            OO00OOO00OOOO0OOO .length -=1 #line:380
            del OO00OOO00OOOO0OOO .datas [len (OO00OOO00OOOO0OOO .datas )-1 ]#line:381
    def empty (O0O0O00000OOO0OOO ):#line:383
        return not bool (O0O0O00000OOO0OOO .length )#line:385
    def __str__ (OOO000000O0OO0O0O ):#line:387
        print ('-----------------------str called----------------------')#line:388
        return ','.join ([str (O0O000OO0OOOOOOOO )for O0O000OO0OOOOOOOO in OOO000000O0OO0O0O .datas ])#line:389
