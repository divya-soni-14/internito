from django.db import models
from django.contrib.auth.models import User

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=80)
    branch = models.CharField(max_length=255,blank=True)
    cgpa_cutoff = models.FloatField(blank=True)
    resume = models.TextField(blank=True)
    batch = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255,blank=False)
    summary = models.TextField(blank=False)
    period = models.CharField(max_length=255,blank=False)
    ot_summary = models.TextField(blank = True)
    ot_question1 = models.TextField(blank = True, null = True)
    ot_question1_link = models.TextField(blank = True, null = True, default = 'NONE')
    ot_question2 = models.TextField(blank = True, null = True)
    ot_question2_link = models.TextField(blank = True, null = True)
    ot_question3 = models.TextField(blank = True, null = True)
    ot_question3_link = models.TextField(blank = True, null = True)
    ot_question4 = models.TextField(blank = True, null = True)
    ot_question4_link = models.TextField(blank = True, null = True)
    round1_details = models.TextField(blank = True, null = True)
    round2_details = models.TextField(blank = True, null = True)
    round3_details = models.TextField(blank = True, null = True)
    final_summary = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.name + '_' + self.company

class Emailverify(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    code=models.IntegerField(null=True,blank=True)
    status=models.BooleanField(null=True,blank=True)
class FeedBack(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=250)
    def __str__(self):
        return self.user.username
