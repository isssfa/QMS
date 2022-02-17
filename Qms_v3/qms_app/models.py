from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=30, unique=True)
    emp_name = models.CharField(max_length=100)
    emp_desi = models.CharField(max_length=100)
    emp_process = models.CharField(max_length=150)
    emp_rm1 = models.CharField(max_length=100)
    emp_rm1_id = models.CharField(max_length=30)
    emp_rm2 = models.CharField(max_length=100)
    emp_rm2_id = models.CharField(max_length=30)
    emp_rm3 = models.CharField(max_length=100)
    emp_rm3_id = models.CharField(max_length=30)
    agent_status = models.CharField(max_length=30)

    def __str__(self):
        return self.emp_name


class Campaign(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=50)
    page_type = models.CharField(max_length=50)
    manager_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='mgr')
    qa_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qa')


class Outbound(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='Outbound', max_length=50)
    page_type = models.CharField(default='Outbound', max_length=50)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)

    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # Opening and Closing
    oc_1 = models.IntegerField()
    oc_2 = models.IntegerField()
    oc_3 = models.IntegerField()
    # SoftSkills
    softskill_1 = models.IntegerField()
    softskill_2 = models.IntegerField()
    softskill_3 = models.IntegerField()
    softskill_4 = models.IntegerField()
    softskill_5 = models.IntegerField()
    # Business and Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()
    compliance_6 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    oc_total = models.IntegerField(null=True)
    softskill_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()

class Inbound(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='Inbound', max_length=50)
    page_type = models.CharField(default='Inbound', max_length=50)
    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    # Customer Experience
    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()
    ce_5 = models.IntegerField()
    ce_6 = models.IntegerField()
    ce_7 = models.IntegerField()
    ce_8 = models.IntegerField()
    ce_9 = models.IntegerField()
    ce_10 = models.IntegerField()
    ce_11 = models.IntegerField()

    # Business
    business_1 = models.IntegerField()
    business_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    ce_total = models.IntegerField(null=True)
    business_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()



class EmailChat(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='Email', max_length=50)
    page_type = models.CharField(default='Email', max_length=50)
    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # questions
    # Customer Experience

    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()
    ce_5 = models.IntegerField()
    ce_6 = models.IntegerField()
    ce_7 = models.IntegerField()
    ce_8 = models.IntegerField()
    ce_9 = models.IntegerField()
    ce_10 = models.IntegerField()
    ce_11 = models.IntegerField()

    # Business
    business_1 = models.IntegerField()
    business_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()

    # Scores
    ce_total = models.IntegerField(null=True)
    business_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)


    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()

class DigitalSwissGold(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='Digital', max_length=50)
    page_type = models.CharField(default='Digital', max_length=50)
    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # questions
    # Customer Experience

    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()
    ce_5 = models.IntegerField()
    ce_6 = models.IntegerField()
    ce_7 = models.IntegerField()
    ce_8 = models.IntegerField()
    ce_9 = models.IntegerField()
    ce_10 = models.IntegerField()
    ce_11 = models.IntegerField()

    # Business
    business_1 = models.IntegerField()
    business_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()

    # Scores
    ce_total = models.IntegerField(null=True)
    business_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()


class FLA(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='FLA', max_length=50)
    page_type = models.CharField(default='FLA', max_length=50)
    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    transaction_handles_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    service = models.CharField(max_length=100)
    concept = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)

    # questions
    check_list = models.IntegerField()

    # Scores
    overall_score = models.IntegerField(null=True)

    reason_for_failure = models.TextField()
    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()


class BlazingHog(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='BlazingHog', max_length=50)
    page_type = models.CharField(default='BlazingHog', max_length=50)
    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    concept = models.CharField(max_length=100)
    email_chat_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    query_type = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=100)


    # questions
    # solutions
    solution_1 = models.IntegerField()
    solution_2 = models.IntegerField()
    solution_3 = models.IntegerField()
    solution_4 = models.IntegerField()

    #Efficiency
    efficiency_1 = models.IntegerField()
    efficiency_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    # Scores
    solution_score = models.IntegerField()
    efficiency_score = models.IntegerField()
    compliance_score = models.IntegerField()
    overall_score = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()

class NoomPod(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='Noompod', max_length=50)
    page_type = models.CharField(default='Noompod', max_length=50)
    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    evaluator_name = models.CharField(max_length=100)
    transaction_handled_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    ticket_number = models.CharField(max_length=50)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    # Customer Experience
    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()
    compliance_6 = models.IntegerField()


    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    ce_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()


class NoomEva(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='Noomeva', max_length=50)
    page_type = models.CharField(default='Noomeva', max_length=50)
    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    evaluator_name = models.CharField(max_length=100)
    transaction_handled_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    ticket_number = models.CharField(max_length=50)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    # Customer Experience
    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()
    compliance_6 = models.IntegerField()


    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    ce_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()


class AbHindalco(models.Model):
    campaign = models.CharField(max_length=150)
    campaign_type = models.CharField(default='Abhindalco', max_length=50)
    page_type = models.CharField(default='Abhindalco', max_length=50)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)

    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)

    # Opening and Closing
    oc_1 = models.IntegerField()
    oc_2 = models.IntegerField()
    oc_3 = models.IntegerField()
    # SoftSkills
    softskill_1 = models.IntegerField()
    softskill_2 = models.IntegerField()
    softskill_3 = models.IntegerField()
    softskill_4 = models.IntegerField()
    # Business and Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()


    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    oc_total = models.IntegerField(null=True)
    softskill_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.TimeField()


