#!/usr/bin/python3
# -*- coding: utf-8 -*-
# python database_setup.py
from new_student_volunteer.models import Person, Activity
# initialize student_list and gender_list
student_list = []
gender_list = []
with open('student2018.txt','rb') as f:
    for byte_str in f:
        unicode_str = byte_str.decode('utf-8')
        str_list = unicode_str.split('\t')
        if(len(str_list[0])<=3):
            student_list.append(str_list[0].strip())
            gender_list.append(str_list[1].strip())
activity_description_list = ['开学典礼签到','开学典礼机动','开学典礼指引（限女生）','29号下午讲座签到CⅡ栋三层大报告厅','29号下午讲座签到一层多功能厅','29号下午讲座签到CI栋101室','29号下午讲座签到CI栋102室','29号晚上讲座签到CⅡ栋三层大报告厅','29号晚上讲座签到一层多功能厅','29号晚上讲座签到CI栋101室','29号晚上讲座签到CI栋102室','30号下午讲座签到CⅡ栋三层大报告厅','30号下午讲座签到一层多功能厅','30号下午讲座签到CI栋101室','30号下午讲座签到CI栋102室','30号晚上讲座签到CⅡ栋三层大报告厅','30号晚上讲座签到一层多功能厅','30号晚上讲座签到CI栋101室','30号晚上讲座签到CI栋102室','31号下午讲座签到CⅡ栋三层大报告厅','31号下午讲座签到一层多功能厅','31号下午讲座签到CI栋101室','31号下午讲座签到CI栋102室']
activity_code = [1,2,3,5,10,15,20,25,50,75,100,125,250,375,500,625,1250,1875,2500,3125,6250,9375,12500]
activity_number = [7,2,2,4,2,2,2,4,2,2,2,4,2,2,2,4,2,2,2,4,2,2,2]
    
# initialization of student_list    
for index, i in enumerate(student_list):
    if(Person.objects.filter(name=i)):
        continue
    else: 
        # create new object
        p = Person(name = i, gender = gender_list[index])
        p.save()
# initialization of activity
for index, i in enumerate(activity_code):
    if not(Activity.objects.filter(code=i)):
        a = Activity(description = activity_description_list[index], required_number = activity_number[index], code = i)
        a.save()
    else:
        a = Activity.objects.get(code=i)
        a.current_number = 0
        a.save()
        