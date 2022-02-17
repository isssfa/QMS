import datetime
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.

# Campaign Models
campaign_list = [Outbound, Inbound, EmailChat, DigitalSwissGold, FLA, BlazingHog, NoomPod, NoomEva, AbHindalco]

# page names must be equal to campaign type
pages = ["Outbound", "Inbound", "Email", "Digital", "FLA", "BlazingHog", "Noompod", "Noomeva", "Abhindalco","new"]

# Calculating first and todays date
currentMonth = datetime.datetime.now().month
currentYear = datetime.datetime.now().year
month_start_date = datetime.datetime(currentYear, currentMonth, 1)
todays_date = date.today()


def index(request):
    logout(request)
    return render(request, "index.html")


def Login(request):
    if request.method == "POST":
        username = request.POST["user"]
        password = request.POST["pass"]
        user = authenticate(username=username, password=password)
        if user is not None:
            # user_login
            login(request, user)
            designation = request.user.profile.emp_desi

            if designation == "QA":
                return redirect("/qa-dashboard")
            else:
                return redirect("/agent-dashboard")
        else:
            messages.info(request, 'Invalid user !')
            return redirect("/")
    else:
        pass


# QA Dashboard (qa-dashboard)
def qaDashboard(request):
    user = request.user
    emp_id = request.user.profile.emp_id

    campaigns = Campaign.objects.filter(qa_id=user)
    out_campaigns = Campaign.objects.filter(qa_id=user, type='Outbound')
    in_campaign = Campaign.objects.filter(qa_id=user, type='Inbound')
    email_campaign = Campaign.objects.filter(qa_id=user, type='Email')
    other_campaign = Campaign.objects.filter(qa_id=user).exclude(type__in=['Outbound', 'Inbound', 'Email'])
    profile = Profile.objects.all()

    # All Audits
    all_total_count = []
    for i in campaign_list:
        campaign = i.objects.filter(added_by=emp_id).count()
        all_total_count.append(campaign)
    all_total = 0
    for i in all_total_count:
        all_total += i

    # All Audits Current Month

    # All Audits Current Month Count
    month_all_count = []
    for i in campaign_list:
        camapign = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date]).count()
        month_all_count.append(camapign)
    month_all_total = 0
    for i in month_all_count:
        month_all_total += i

    # Month's Average Score
    camapign_score = 0
    for i in campaign_list:
        score = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
        for j in score:
            camapign_score += j.overall_score
    if month_all_total == 0:
        score_average = "No Audits This Month"
    else:
        score_average = (camapign_score) / month_all_total

    # Month's Fatal Count
    fatal_count = 0
    for i in campaign_list:
        fatal = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
        for j in fatal:
            fatal_count += j.fatal_count

    # Open Audits
    open_count = []
    for i in campaign_list:
        campaign = i.objects.filter(added_by=emp_id, status=False).count()
        open_count.append(campaign)
    open_total = 0
    for i in open_count:
        open_total += i

    # Dispute Audits
    dispute_count = []
    for i in campaign_list:
        campaign = i.objects.filter(added_by=emp_id, dispute_status=True).count()
        dispute_count.append(campaign)
    dispute_total = 0
    for i in dispute_count:
        dispute_total += i

    # Fatal Audits
    fatal_audit_count = []
    for i in campaign_list:
        campaign = i.objects.filter(added_by=emp_id, fatal=True,
                                    audit_date__range=[month_start_date, todays_date]).count()
        fatal_audit_count.append(campaign)
    fatal_total = 0
    for i in fatal_audit_count:
        fatal_total += i

    # Coaching Closure
    closure_count_list = []
    for i in campaign_list:
        campaign = i.objects.filter(added_by=emp_id, status=True).count()
        closure_count_list.append(campaign)
    closure_count = 0
    for i in closure_count_list:
        closure_count += i

    if all_total == 0:
        coaching_closure = "No Audits"
    else:
        coaching_closure = (closure_count / all_total) * 100

    tot = []
    for i in campaign_list:
        campaign = i.objects.filter(added_by=emp_id, status=False)
        tot.append(campaign)

    data = {"campaigns": campaigns, "out_campaigns": out_campaigns, "profile": profile, "in_campaign": in_campaign,
            "email_campaign": email_campaign, "other_campaign": other_campaign, "audit": tot,
            "month_all_total": month_all_total, "open_total": open_total, "dispute_total": dispute_total,
            "average": score_average, "fatal": fatal_count,
            "all_total": all_total, "fatal_total": fatal_total, "coaching_closure": coaching_closure}

    return render(request, "qa_dashboard.html", data)


# Test function for ajax (get-emp)
def getEmp(request):
    if request.method == "POST":
        campaign = request.POST.get("campaign")
        profile = Profile.objects.filter(emp_process=campaign)
        return JsonResponse({"profile": profile}, status=200)


# QA Report Page (qa-reports/<str:type>)
def ReportTable(request, type):
    emp_id = request.user.profile.emp_id

    def auditcalculator(type):
        audits = []
        if type == 'all':
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id)
                audits.append(tot_obj)
        elif type == "fatal":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, fatal=True,
                                           audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "month":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "open":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, status=False)
                audits.append(tot_obj)
        elif type == "dispute":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, dispute_status=True)
                audits.append(tot_obj)
        elif type == "campaign-range":
            if request.method == "POST":
                cname = request.POST.get("campaign")
                status = request.POST.get("status")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                for i in campaign_list:
                    if start_date:
                        if cname == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id, audit_date__range=[start_date, end_date])
                        elif cname == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False,
                                                       audit_date__range=[start_date, end_date])
                        elif cname and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, campaign=cname, status=False,
                                                       audit_date__range=[start_date, end_date])
                        else:
                            tot_obj = i.objects.filter(campaign=cname, added_by=emp_id,
                                                       audit_date__range=[start_date, end_date])
                        audits.append(tot_obj)
                    else:
                        if cname == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id)
                        elif cname == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False)
                        elif cname and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, campaign=cname, status=False)
                        else:
                            tot_obj = i.objects.filter(campaign=cname, added_by=emp_id)
                        audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")

        elif type == "emp-range":
            if request.method == "POST":
                emp = request.POST.get("emp_id")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                status = request.POST.get("status")

                for i in campaign_list:
                    if start_date:
                        if emp == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id, audit_date__range=[start_date, end_date])
                        elif emp == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False,
                                                       audit_date__range=[start_date, end_date])
                        elif emp and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, emp_id=emp, status=False,
                                                       audit_date__range=[start_date, end_date])
                        else:
                            tot_obj = i.objects.filter(emp_id=emp, added_by=emp_id,
                                                       audit_date__range=[start_date, end_date])
                        audits.append(tot_obj)
                    else:
                        if emp == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id)
                        elif emp == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False)
                        elif emp and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, emp_id=emp, status=False)
                        else:
                            tot_obj = i.objects.filter(emp_id=emp, added_by=emp_id)
                        audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")
        else:
            messages.info(request, 'Invalid Request. You have been logged out :)')
            logout(request)
            return redirect("/")

        return audits

    audits = auditcalculator(type)
    data = {"audit": audits, "type": type}
    return render(request, "qa_reports.html", data)


# Form View (form)
def formView(request):
    if request.method == "POST":
        campaign = request.POST["campaign"]
        emp = request.POST["emp"]
        campaign = Campaign.objects.get(name=campaign)
        type = campaign.page_type
        profile = Profile.objects.get(emp_id=emp)
        today = date.today()
        start = str(datetime.datetime.now().time())
        data = {"campaign": campaign, "profile": profile, "today": today, "start_time": start}

        for j in pages:
            if j == type:
                return render(request, "form/" + j + ".html", data)

    else:
        messages.info(request, 'Invalid Request !')
        logout(request)
        return redirect("/")


# Report for QA (report)
def qaReport(request):
    if request.method == "POST":
        id = request.POST["id"]
        type = request.POST["type"]

        for i in campaign_list:
            obj = i.objects.all()
            if obj.count() > 0:
                if obj[0].page_type == type:
                    campaign = i.objects.get(id=id)
                    data = {"form": campaign}
                    for j in pages:
                        if type == j:
                            return render(request, "report/" + j + ".html", data)
                else:
                    pass
            else:
                pass

    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


# Agent Dashbaoard (agent-dashboard)
def agentDashbaoard(request):
    emp_id = request.user.profile.emp_id

    # All Audits
    all_total_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id).count()
        all_total_count.append(campaign)
    all_total = 0
    for i in all_total_count:
        all_total += i

    # All Audits Current Month

    # All Audits Current Month Count
    month_all_count = []
    for i in campaign_list:
        camapign = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date]).count()
        month_all_count.append(camapign)
    month_all_total = 0
    for i in month_all_count:
        month_all_total += i

    # Month's Average Score
    camapign_score = 0
    for i in campaign_list:
        score = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
        for j in score:
            camapign_score += j.overall_score
    if month_all_total == 0:
        score_average = "No Audits This Month"
    else:
        score_average = (camapign_score) / month_all_total

    # Month's Fatal Count
    fatal_count = 0
    for i in campaign_list:
        fatal = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
        for j in fatal:
            fatal_count += j.fatal_count

    # Open Audits
    open_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, status=False).count()
        open_count.append(campaign)
    open_total = 0
    for i in open_count:
        open_total += i

    # Dispute Audits
    dispute_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, dispute_status=True).count()
        dispute_count.append(campaign)
    dispute_total = 0
    for i in dispute_count:
        dispute_total += i

    # Fatal Audits
    fatal_audit_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, fatal=True,
                                    audit_date__range=[month_start_date, todays_date]).count()
        fatal_audit_count.append(campaign)
    fatal_total = 0
    for i in fatal_audit_count:
        fatal_total += i

    # Coaching Closure
    closure_count_list = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, status=True).count()
        closure_count_list.append(campaign)
    closure_count = 0
    for i in closure_count_list:
        closure_count += i

    if all_total == 0:
        coaching_closure = "No Audits"
    else:
        coaching_closure = (closure_count / all_total) * 100

    tot = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, status=False)
        tot.append(campaign)

    data = {
        "audit": tot, "month_all_total": month_all_total, "open_total": open_total, "dispute_total": dispute_total,
        "average": score_average, "fatal": fatal_count,
        "all_total": all_total, "fatal_total": fatal_total, "coaching_closure": coaching_closure
    }
    return render(request, "agent_dashboard.html", data)


# Agent Report Table (emp-report/<str:type>)
def agentReportTable(request, type):
    emp_id = request.user.profile.emp_id

    def auditcalculator(type):
        audits = []
        if type == 'all':
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id)
                audits.append(tot_obj)
        elif type == "fatal":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, fatal=True, audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "month":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "open":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, status=False)
                audits.append(tot_obj)
        elif type == "dispute":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, dispute_status=True)
                audits.append(tot_obj)
        elif type == "range":
            if request.method == "POST":
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                for i in campaign_list:
                    tot_obj = i.objects.filter(emp_id=emp_id, audit_date__range=[start_date, end_date])
                    audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")
        else:
            messages.info(request, 'Invalid Request.')
            return redirect("/")
        return audits

    audits = auditcalculator(type)
    data = {"audit": audits, "type": type}
    return render(request, "agent_reports.html", data)


# Agent Report (agent-report)
def agentReport(request):
    if request.method == "POST":
        id = request.POST["id"]
        type = request.POST["type"]

        for i in campaign_list:
            obj = i.objects.all()
            if obj.count() > 0:
                if obj[0].page_type == type:
                    campaign = i.objects.get(id=id)
                    data = {"form": campaign, "type": type}
                    for j in pages:
                        if type == j:
                            return render(request, "agent/" + j + ".html", data)
                else:
                    pass
            else:
                pass

    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


# Agent Respond
def agentRespond(request):
    now = date.today()
    if request.method == "POST":
        id = request.POST["id"]
        emp_com_accept = request.POST.get("emp_com_accept")
        emp_com_reject = request.POST.get("emp_com_reject")
        type = request.POST["type"]

        for i in campaign_list:
            obj = i.objects.all()
            if obj.count() > 0:
                if obj[0].campaign_type == type:
                    campaign = i
                else:
                    pass
            else:
                pass

        e = campaign.objects.get(id=id)

        if emp_com_accept:
            e.emp_comments = emp_com_accept
            e.status = True
            e.dispute_status = False
            e.closed_date = now
        if emp_com_reject:
            e.emp_comments = emp_com_reject
            e.status = False
            e.dispute_status = True
        e.save()
        messages.warning(request, 'Your response have been captured successfully!')
        return redirect("/agent-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


# Outbound Form Submit
def outboundFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        opening_ques_1 = int(request.POST["oc_1"])
        opening_ques_2 = int(request.POST["oc_2"])
        opening_ques_3 = int(request.POST["oc_3"])
        openng_score = opening_ques_1 + opening_ques_2 + opening_ques_3

        softskills_ques_1 = int(request.POST["softskill_1"])
        softskills_ques_2 = int(request.POST["softskill_2"])
        softskills_ques_3 = int(request.POST["softskill_3"])
        softskills_ques_4 = int(request.POST["softskill_4"])
        softskills_ques_5 = int(request.POST["softskill_5"])
        softskill_score = softskills_ques_1 + softskills_ques_2 + softskills_ques_3 + softskills_ques_4 + softskills_ques_5

        business_compliance_qus_1 = int(request.POST["compliance_1"])
        business_compliance_qus_2 = int(request.POST["compliance_2"])
        business_compliance_qus_3 = int(request.POST["compliance_3"])
        business_compliance_qus_4 = int(request.POST["compliance_4"])
        business_compliance_qus_5 = int(request.POST["compliance_5"])
        business_compliance_qus_6 = int(request.POST["compliance_6"])
        business_compliance_score = business_compliance_qus_1 + business_compliance_qus_2 + business_compliance_qus_3 + business_compliance_qus_4 + business_compliance_qus_5 + business_compliance_qus_6

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [business_compliance_qus_1, business_compliance_qus_2, business_compliance_qus_3,
                      business_compliance_qus_4, business_compliance_qus_5, business_compliance_qus_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if business_compliance_qus_1 == 0 or business_compliance_qus_2 == 0 or business_compliance_qus_3 == 0 or business_compliance_qus_4 == 0 or business_compliance_qus_5 == 0 or business_compliance_qus_6 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = openng_score + softskill_score + business_compliance_score
            fatal = False
        added_by = request.user.profile.emp_id
        e = Outbound()
        e.audit_duration = duration
        e.oc_total = openng_score
        e.softskill_total = softskill_score
        e.compliance_total = business_compliance_score
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.oc_1 = opening_ques_1
        e.oc_2 = opening_ques_2
        e.oc_3 = opening_ques_3
        e.softskill_1 = softskills_ques_1
        e.softskill_2 = softskills_ques_2
        e.softskill_3 = softskills_ques_3
        e.softskill_4 = softskills_ques_4
        e.softskill_5 = softskills_ques_5
        e.compliance_1 = business_compliance_qus_1
        e.compliance_2 = business_compliance_qus_2
        e.compliance_3 = business_compliance_qus_3
        e.compliance_4 = business_compliance_qus_4
        e.compliance_5 = business_compliance_qus_5
        e.compliance_6 = business_compliance_qus_6
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)
        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


# Inbound Form Submit
def inboundFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_5 = int(request.POST["ce_5"])
        ce_6 = int(request.POST["ce_6"])
        ce_7 = int(request.POST["ce_7"])
        ce_8 = int(request.POST["ce_8"])
        ce_9 = int(request.POST["ce_9"])
        ce_10 = int(request.POST["ce_10"])
        ce_11 = int(request.POST["ce_11"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4 + ce_5 + ce_6 + ce_7 + ce_8 + ce_9 + ce_10 + ce_11

        business_1 = int(request.POST["business_1"])
        business_2 = int(request.POST["business_2"])
        business_score = business_1 + business_2

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + business_score + compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        e = Inbound()
        e.audit_duration = duration
        e.ce_total = ce_total
        e.business_total = business_score
        e.compliance_total = compliance_score
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week

        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.ce_5 = ce_5
        e.ce_6 = ce_6
        e.ce_7 = ce_7
        e.ce_8 = ce_8
        e.ce_9 = ce_9
        e.ce_10 = ce_10
        e.ce_11 = ce_11

        e.business_1 = business_1
        e.business_2 = business_2

        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5

        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


# Email Form Submit
def emailFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_5 = int(request.POST["ce_5"])
        ce_6 = int(request.POST["ce_6"])
        ce_7 = int(request.POST["ce_7"])
        ce_8 = int(request.POST["ce_8"])
        ce_9 = int(request.POST["ce_9"])
        ce_10 = int(request.POST["ce_10"])
        ce_11 = int(request.POST["ce_11"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4 + ce_5 + ce_6 + ce_7 + ce_8 + ce_9 + ce_10 + ce_11

        business_1 = int(request.POST["business_1"])
        business_2 = int(request.POST["business_2"])
        business_score = business_1 + business_2

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + business_score + compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        e = EmailChat()
        e.audit_duration = duration
        e.ce_total = ce_total
        e.business_total = business_score
        e.compliance_total = compliance_score
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week

        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.ce_5 = ce_5
        e.ce_6 = ce_6
        e.ce_7 = ce_7
        e.ce_8 = ce_8
        e.ce_9 = ce_9
        e.ce_10 = ce_10
        e.ce_11 = ce_11

        e.business_1 = business_1
        e.business_2 = business_2

        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5

        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


def DigitalSwissGoldFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_5 = int(request.POST["ce_5"])
        ce_6 = int(request.POST["ce_6"])
        ce_7 = int(request.POST["ce_7"])
        ce_8 = int(request.POST["ce_8"])
        ce_9 = int(request.POST["ce_9"])
        ce_10 = int(request.POST["ce_10"])
        ce_11 = int(request.POST["ce_11"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4 + ce_5 + ce_6 + ce_7 + ce_8 + ce_9 + ce_10 + ce_11

        business_1 = int(request.POST["business_1"])
        business_2 = int(request.POST["business_2"])
        business_score = business_1 + business_2

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + business_score + compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        e = DigitalSwissGold()
        e.audit_duration = duration
        e.ce_total = ce_total
        e.business_total = business_score
        e.compliance_total = compliance_score
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week

        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.ce_5 = ce_5
        e.ce_6 = ce_6
        e.ce_7 = ce_7
        e.ce_8 = ce_8
        e.ce_9 = ce_9
        e.ce_10 = ce_10
        e.ce_11 = ce_11

        e.business_1 = business_1
        e.business_2 = business_2

        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5

        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


def FLAFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]
        transaction_handles_date = request.POST["transdate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        service = request.POST["service"]
        order_id = request.POST["order_id"]

        check_list = int(request.POST["checklist_1"])

        reason_for_failure = request.POST["reason_for_failure"]
        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [check_list]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if check_list == 0:
            total_score = 0
            fatal = True
        else:
            total_score = check_list
            fatal = False
        added_by = request.user.profile.emp_id

        e = FLA()
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.transaction_handles_date = transaction_handles_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.reason_for_failure = reason_for_failure
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.service = service
        e.order_id = order_id
        e.check_list = check_list
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


def blazingHogFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]
        zone = request.POST["zone"]
        customer_name = request.POST["customer"]

        email_chat_date = request.POST["calldate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        query_type = request.POST["query_type"]
        ticket_id = request.POST["ticketnumber"]

        solution_1 = int(request.POST["solution_1"])
        solution_2 = int(request.POST["solution_2"])
        solution_3 = int(request.POST["solution_3"])
        solution_4 = int(request.POST["solution_4"])
        solution_score = solution_1 + solution_2 + solution_3 + solution_4
        efficiency_1 = int(request.POST["efficiency_1"])
        efficiency_2 = int(request.POST["efficiency_2"])
        efficiency_score = efficiency_1 + efficiency_2
        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_score = compliance_1 + compliance_2 + compliance_3

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = solution_score + efficiency_score + compliance_score
            fatal = False

        added_by = request.user.profile.emp_id

        e = BlazingHog()
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.email_chat_date = email_chat_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.zone = zone
        e.customer_name = customer_name
        e.query_type = query_type
        e.ticket_id = ticket_id
        e.solution_1 = solution_1
        e.solution_2 = solution_2
        e.solution_3 = solution_3
        e.solution_4 = solution_4
        e.efficiency_1 = efficiency_1
        e.efficiency_2 = efficiency_2
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.solution_score = solution_score
        e.efficiency_score = efficiency_score
        e.compliance_score = compliance_score
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


def NoomPodFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]

        transaction_handled_date = request.POST["transdate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        evaluator_name = request.POST["evaluator"]
        ticket_number = request.POST["ticketnumber"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_6 = int(request.POST["compliance_6"])
        compliance_total = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5 + compliance_6

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5, compliance_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0 or compliance_6 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + compliance_total
            fatal = False

        added_by = request.user.profile.emp_id

        e = NoomPod()
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.transaction_handled_date = transaction_handled_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.evaluator_name = evaluator_name
        e.ticket_number = ticket_number
        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5
        e.compliance_6 = compliance_6
        e.ce_total = ce_total
        e.compliance_total = compliance_total
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


def NoomEvaFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]

        transaction_handled_date = request.POST["transdate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        evaluator_name = request.POST["evaluator"]
        ticket_number = request.POST["ticketnumber"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_6 = int(request.POST["compliance_6"])
        compliance_total = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5 + compliance_6

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5, compliance_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0 or compliance_6 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + compliance_total
            fatal = False

        added_by = request.user.profile.emp_id

        e = NoomEva()
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.transaction_handled_date = transaction_handled_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.evaluator_name = evaluator_name
        e.ticket_number = ticket_number
        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5
        e.compliance_6 = compliance_6
        e.ce_total = ce_total
        e.compliance_total = compliance_total
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


def AbHindalcoFormSubmit(request):
    if request.method == "POST":
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign = request.POST["campaign_name"]
        campaign_type = request.POST["campaign_type"]
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]

        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        opening_ques_1 = int(request.POST["oc_1"])
        opening_ques_2 = int(request.POST["oc_2"])
        opening_ques_3 = int(request.POST["oc_3"])
        openng_score = opening_ques_1 + opening_ques_2 + opening_ques_3

        softskills_ques_1 = int(request.POST["softskill_1"])
        softskills_ques_2 = int(request.POST["softskill_2"])
        softskills_ques_3 = int(request.POST["softskill_3"])
        softskills_ques_4 = int(request.POST["softskill_4"])
        softskill_score = softskills_ques_1 + softskills_ques_2 + softskills_ques_3 + softskills_ques_4

        business_compliance_qus_1 = int(request.POST["compliance_1"])
        business_compliance_qus_2 = int(request.POST["compliance_2"])
        business_compliance_qus_3 = int(request.POST["compliance_3"])
        business_compliance_qus_4 = int(request.POST["compliance_4"])
        business_compliance_score = business_compliance_qus_1 + business_compliance_qus_2 + business_compliance_qus_3 + business_compliance_qus_4

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [opening_ques_2, business_compliance_qus_2, business_compliance_qus_3, business_compliance_qus_4]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if opening_ques_2 == 0 or business_compliance_qus_2 == 0 or business_compliance_qus_3 == 0 or business_compliance_qus_4 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = openng_score + softskill_score + business_compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        e = AbHindalco()
        e.audit_duration = duration
        e.oc_total = openng_score
        e.softskill_total = softskill_score
        e.compliance_total = business_compliance_score
        e.overall_score = total_score
        e.campaign = campaign
        e.campaign_type = campaign_type
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.oc_1 = opening_ques_1
        e.oc_2 = opening_ques_2
        e.oc_3 = opening_ques_3
        e.softskill_1 = softskills_ques_1
        e.softskill_2 = softskills_ques_2
        e.softskill_3 = softskills_ques_3
        e.softskill_4 = softskills_ques_4
        e.compliance_1 = business_compliance_qus_1
        e.compliance_2 = business_compliance_qus_2
        e.compliance_3 = business_compliance_qus_3
        e.compliance_4 = business_compliance_qus_4
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)
        return redirect("/qa-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        logout(request)
        return redirect("/")


