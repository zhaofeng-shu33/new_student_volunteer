#!/usr/bin/python3
# -*- coding: utf-8 -*-
# python render_result.py
# file-description: generate rendered html table of allocation
from django.conf import settings
import django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './db.sqlite3',
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]
settings.configure(DEBUG=True, INSTALLED_APPS=['new_student_volunteer'], DATABASES=DATABASES, TEMPLATES=TEMPLATES)
django.setup()
from new_student_volunteer.models import Person, Activity, decode_job_id, decode_activity
from django.template import loader
def result():
    context = {}
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
    template = loader.get_template('new_student_volunteer/render_result_template.html')  
    context['positions'] = positions
    return template.render(context)
    
open('result_rendered.html','wb').write(result().encode('utf-8'))