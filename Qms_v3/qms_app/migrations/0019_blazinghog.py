# Generated by Django 4.0.1 on 2022-01-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qms_app', '0018_alter_fla_campaign_type_alter_fla_page_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlazingHog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(max_length=150)),
                ('campaign_type', models.CharField(default='BlazingHog', max_length=50)),
                ('page_type', models.CharField(default='BlazingHog', max_length=50)),
                ('emp_id', models.CharField(max_length=30)),
                ('associate_name', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('customer_name', models.CharField(max_length=100)),
                ('concept', models.CharField(max_length=100)),
                ('email_chat_date', models.DateField()),
                ('audit_date', models.DateField()),
                ('quality_analyst', models.CharField(max_length=100)),
                ('team_lead', models.CharField(max_length=100)),
                ('team_lead_id', models.CharField(max_length=30)),
                ('manager', models.CharField(max_length=100)),
                ('manager_id', models.CharField(max_length=30)),
                ('am', models.CharField(max_length=100)),
                ('am_id', models.CharField(max_length=30)),
                ('week', models.CharField(max_length=10)),
                ('query_type', models.CharField(max_length=100)),
                ('ticket_id', models.CharField(max_length=100)),
                ('solution_1', models.IntegerField()),
                ('solution_2', models.IntegerField()),
                ('solution_3', models.IntegerField()),
                ('solution_4', models.IntegerField()),
                ('efficiency_1', models.IntegerField()),
                ('efficiency_2', models.IntegerField()),
                ('compliance_1', models.IntegerField()),
                ('compliance_2', models.IntegerField()),
                ('compliance_3', models.IntegerField()),
                ('solution_score', models.IntegerField()),
                ('efficiency_score', models.IntegerField()),
                ('compliance_score', models.IntegerField()),
                ('overall_score', models.IntegerField()),
                ('areas_improvement', models.TextField()),
                ('positives', models.TextField()),
                ('comments', models.TextField()),
                ('added_by', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(null=True)),
                ('emp_comments', models.TextField(null=True)),
                ('fatal', models.BooleanField(default=False)),
                ('fatal_count', models.IntegerField(default=0)),
                ('dispute_status', models.BooleanField(default=False)),
                ('audit_duration', models.TimeField()),
            ],
        ),
    ]
