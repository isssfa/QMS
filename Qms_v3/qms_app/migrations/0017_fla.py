# Generated by Django 4.0.1 on 2022-01-25 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qms_app', '0016_campaign_page_type_digitalswissgold_page_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FLA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(max_length=150)),
                ('campaign_type', models.CharField(default='Digital', max_length=50)),
                ('page_type', models.CharField(default='Digital', max_length=50)),
                ('emp_id', models.CharField(max_length=30)),
                ('associate_name', models.CharField(max_length=50)),
                ('transaction_handles_date', models.DateField()),
                ('audit_date', models.DateField()),
                ('quality_analyst', models.CharField(max_length=100)),
                ('team_lead', models.CharField(max_length=100)),
                ('team_lead_id', models.CharField(max_length=30)),
                ('manager', models.CharField(max_length=100)),
                ('manager_id', models.CharField(max_length=30)),
                ('am', models.CharField(max_length=100)),
                ('am_id', models.CharField(max_length=30)),
                ('week', models.CharField(max_length=10)),
                ('service', models.CharField(max_length=100)),
                ('concept', models.CharField(max_length=100)),
                ('order_id', models.CharField(max_length=100)),
                ('check_list', models.IntegerField()),
                ('overall_score', models.IntegerField(null=True)),
                ('reason_for_failure', models.TextField()),
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
