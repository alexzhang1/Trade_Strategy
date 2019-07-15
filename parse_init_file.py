# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:10:58 2019

@author: zhangwei
"""

import os
import re
import pandas as pd

filename = 'sina_exter_code.txt'
result=[]
exter_code_list = []
erter_name_list = []
unit_chg_rate = []
unit_chg_name = []
with open(filename, "r", encoding='UTF-8') as f:
    for line in f.readlines():
#        temp_list = line.split(':')
#        temp_list2 = [(str(i).strip('\t')) for i in temp_list]
#        exter_code_list.append(temp_list2[0])
#        print(temp_list2[0], temp_list2[1])
#        for item in temp_list2[1]:
#            temp3
#        result.append(temp_list2)
        #	NAS: ["纳指期货", [0]],
        #	NID: ["LME镍3个月", [1, "美元/吨"]],
#        print(line)
#        matchObj = re.match( r'(.*): ["(.*)", [(.*)]],', line, re.M|re.I)
        matchObj = re.match( r'(.*): \["(.*)", \[(.*)]],', line, re.M|re.I)
        print(matchObj)
        if matchObj:
#            print("matchObj.group() : ", matchObj.group())
#            print("matchObj.group(1) : ", matchObj.group(1))
#            print("matchObj.group(2) : ", matchObj.group(2))
#            print("matchObj.group(3) : ", matchObj.group(3))
            exter_code_list.append(matchObj.group(1).strip())
            erter_name_list.append(matchObj.group(2).strip())
            if(matchObj.group(3) != str(0)):
                unit_list = matchObj.group(3).split(',')
                print(unit_list[0], unit_list[1].replace('"','').strip())
                unit_chg_rate.append(float(unit_list[0]))
                unit_chg_name.append(unit_list[1].replace('"','').strip())
            else:
                unit_chg_rate.append(0)
                unit_chg_name.append(0)  
tem_dict = {"variety_code": exter_code_list, "variety_name": erter_name_list, "unit_chg_rate": unit_chg_rate, "unit_name": unit_chg_name}

variety_df = pd.DataFrame(tem_dict, columns=['variety_code', 'variety_name', 'unit_chg_rate', 'unit_name'])         

variety_df.to_csv('exter_variety.csv',index= False)
             
#print(result)