from django.db import models

# Create your models here.
def decode_job_id(num):
    code_5 = ''
    tmp = num
    while(tmp>0):
        code_5 += str(tmp%5)
        tmp = tmp//5
    code_5_after = '0'*(6 - len(code_5))
    code_5 += code_5_after
    return code_5 
def decode_activity(num):
    # return tuple representation
    tmp = num
    remainder = tmp%5
    cnt = 0
    while(remainder == 0):
        tmp = tmp//5
        remainder = tmp%5 
        cnt += 1
    return (cnt+1, remainder)

class Person(models.Model):
    name = models.CharField(max_length=4)
    gender = models.CharField(max_length=1, choices=(('M','Male'),('F', 'Female')), default='M')
    job_id = models.IntegerField(default=0)
    def __str__(self):
        return '(%s,%s,%s)'%(self.name, self.gender, decode_job_id(self.job_id))

class Activity(models.Model):
    description = models.CharField(max_length=30)
    required_number = models.IntegerField(default=0)
    current_number = models.IntegerField(default=0)    
    code = models.IntegerField(default = 0)
    def __str__(self):#
        between_group_id,within_group_id = decode_activity(self.code)
        return '(%s,%d/%d, %d-%d)'%(self.description, self.current_number, self.required_number,between_group_id,within_group_id)