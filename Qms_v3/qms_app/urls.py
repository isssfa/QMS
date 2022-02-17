
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login', Login),
    path('qa-dashboard', qaDashboard),
    path('get-emp', getEmp),
    path('form', formView),
    path('outbound-submit', outboundFormSubmit),
    path('qa-reports/<str:type>', ReportTable),
    path('report', qaReport),
    path('agent-dashboard', agentDashbaoard),
    path('emp-report/<str:type>', agentReportTable),
    path('agent-report', agentReport),
    path('agent-respond', agentRespond),
    path('inbound-submit', inboundFormSubmit),
    path('email-submit', emailFormSubmit),
    path('digital-submit',DigitalSwissGoldFormSubmit),
    path('fla-submit', FLAFormSubmit),
    path('blazinghog-submit', blazingHogFormSubmit),
    path('noompod-submit',NoomPodFormSubmit),
    path('noomeva-submit',NoomEvaFormSubmit),
    path('abhindalco-submit', AbHindalcoFormSubmit)
]
