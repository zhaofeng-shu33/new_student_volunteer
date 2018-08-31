from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from new_student_volunteer.models import Person, Activity,decode_job_id,decode_activity
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.
def encode5(num_list):
    result = 0
    base_pow = 1
    for i in num_list:
        result += base_pow*int(i)
        base_pow *= 5
    return result

@ensure_csrf_cookie    
def index(request):    
    context = {}
    rq=request.POST
    if(rq):     # 'post' method processing   
        volunteer_name=rq.get('vn','$0')
        position_id_text=rq.get('id','$1') 
        error_str = ''
        # check whether volunteer name exists in the table
        if not Person.objects.filter(name=volunteer_name):
            error_str += 'Name %s does not exist in the database.'%volunteer_name
        print('position_id_text', position_id_text)
        code_list = position_id_text.split(',')
        for i in range(len(code_list)):
            try:            
                code_list[i] = int(code_list[i])
            except ValueError as e:
                error_str += 'invalid position_id_text %s.'%code_list[i]
                break
        if error_str == '': # update the database
            p = Person.objects.get(name=volunteer_name)
            # decode and check for contradiction
            # handle change of applications

            job_id_str = ['0']*6
            # process the new choice
            for code in code_list:
                between_group_id,within_group_id = decode_activity(code)
                if(job_id_str[between_group_id - 1]!='0'):
                    error_str += 'you apply two group %d activities. They are (%s,%s).'%(between_group_id,within_group_id,job_id_str[between_group_id - 1])
                else:
                    job_id_str[between_group_id - 1] = str(within_group_id)
            if(p.gender == 'M' and job_id_str[0] == '3'):# gender restriction for specific case
                error_str += 'Sorry, you are male, and cannot apply for position_id = 3.'
            if(error_str == '' and p.job_id != 0): # already has applications, delete all of them
                jobstr = decode_job_id(p.job_id)
                print("previous jobstr: %s"%jobstr)
                for index,i in enumerate(jobstr):
                    if(i != '0'):
                        activity_id = int(int(i)* pow(5,index))
                        a_pre = Activity.objects.get(code=activity_id)
                        a_pre.current_number -= 1
                        a_pre.save()                
            if(error_str == ''):
                print("current jobstr: %s"%job_id_str)
                p.job_id = encode5(job_id_str)
                p.save()
                for index,i in enumerate(job_id_str): # update the activity
                    if(i != '0'):
                        activity_id = int(int(i)* pow(5,index))
                        a_current = Activity.objects.get(code=activity_id)
                        a_current.current_number += 1
                        a_current.save()            

        positions = []

        for i in Activity.objects.all():
            one_item = {'content':i.description,'total_number':i.required_number}
            name_list = ''
            between_group_id,within_group_id = decode_activity(i.code)
            for j in Person.objects.all():
                job_str = decode_job_id(j.job_id)
                if(job_str[between_group_id-1] == str(within_group_id)):
                    name_list += j.name + ','
            name_list = name_list.strip(',')
            one_item['name_list'] = name_list
            positions.append(one_item)
        template = loader.get_template('new_student_volunteer/result.html')  
        context['error_str'] = error_str      
    else: # get method
        positions = []
        for i in Activity.objects.all():
            positions.append({'content':i.description,'left_number':i.required_number - i.current_number, 'code':i.code})
        template = loader.get_template('new_student_volunteer/index.html')
    context['positions'] = positions
    return HttpResponse(template.render(context, request))