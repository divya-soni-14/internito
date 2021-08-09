from django.db import models

class Experience(models.Model):
    name = models.CharField(max_length=80)
    branch = models.CharField(max_length=255,blank=True)
    cgpa_cutoff = models.FloatField(blank=True)
    company = models.CharField(max_length=255,blank=False)
    summary = models.TextField(blank=False)
    period = models.CharField(max_length=255,blank=False)
    ot_summary = models.TextField(blank = True)
    ot_question1 = models.TextField(blank = True)
    ot_question1_link = models.TextField(blank = True)
    ot_question2 = models.TextField(blank = True)
    ot_question2_link = models.TextField(blank = True)
    ot_question3 = models.TextField(blank = True)
    ot_question3_link = models.TextField(blank = True)
    ot_question4 = models.TextField(blank = True)
    ot_question4_link = models.TextField(blank = True)
    round1_details = models.TextField(blank = True)
    round2_details = models.TextField(blank = True)
    round3_details = models.TextField(blank = True)
    final_summary = models.TextField(blank = True)
    
    def __str__(self):
        return self.name + '_' + self.company
    
