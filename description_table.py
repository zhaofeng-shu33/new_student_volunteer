#!/usr/bin/python
# -*- coding: utf-8 -*-
# python description_table.py
# file-description: generate result which can be copied to excel
from django.conf import settings
import django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './db.sqlite3',
    }
}
settings.configure(DEBUG=True, INSTALLED_APPS=['new_student_volunteer'], DATABASES=DATABASES )
django.setup()
gender_map={'M':'男','F':'女'}
from new_student_volunteer.models import Person, Activity,decode_activity,decode_job_id
csv_str = ''
for index, i in enumerate(Activity.objects.all()):
    between_group_id,within_group_id = decode_activity(i.code)
    for j in Person.objects.all():
        job_str = decode_job_id(j.job_id)        
        if(job_str[between_group_id-1] == str(within_group_id)):
            Ls = [str(index+1)]
            Ls.append(i.description)
            Ls.append(j.name)
            Ls.append('')
            Ls.append(gender_map[j.gender])
            csv_str += '\t'.join(Ls) + '\n'

open('csv_str.txt','wb').write(csv_str.encode('utf-8'))        
        