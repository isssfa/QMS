from django.contrib import admin
from .models import *
# Register your models here

class ProfileSearch(admin.ModelAdmin):
    search_fields = ('emp_name','emp_id')
    list_display = ('emp_name','emp_id', 'emp_desi','emp_process',"emp_rm1_id","emp_rm2_id","emp_rm3_id")


class CampaignSearch(admin.ModelAdmin):
    search_fields = ('name', 'type')
    list_display = ('name', 'type', 'manager_id', 'qa_id')


class OutboundSearch(admin.ModelAdmin):
    search_fields = ('campaign', 'associate_name', 'emp_id')
    list_display = ('associate_name', 'campaign', 'emp_id', 'quality_analyst','overall_score')


admin.site.register(Campaign, CampaignSearch)
admin.site.register(Profile, ProfileSearch)
admin.site.register(Outbound, OutboundSearch)
admin.site.register(Inbound, OutboundSearch)
admin.site.register(EmailChat, OutboundSearch)
admin.site.register(DigitalSwissGold, OutboundSearch)
admin.site.register(FLA, OutboundSearch)
admin.site.register(BlazingHog, OutboundSearch)
admin.site.register(NoomPod, OutboundSearch)
admin.site.register(NoomEva, OutboundSearch)



