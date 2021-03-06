from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import auth
from django.conf import settings
from accounts.models import User
import team_eds
from .models import *
from hr_features.models import *

def check_team_ed(user):
    if user.user_type == 'TEAM_ED':
        return True
    else:
	    return False


def signup(request):
    if request.method == 'POST':
        user = User(fullname=request.POST['fname'],email=request.POST['email'],is_admin=True, user_type='TEAM_ED')
        user.set_password(request.POST['pwd'])
        user.save()
        team=TeamEDS(team_name=request.POST['tname'],head_user=user)
        team.save()
        auth.login(request,user,backend=None)
        return redirect('teams_eds_view_hrs')
    else:
        return render(request,'team_eds/signup.html')
        

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pwd']
        user = auth.authenticate(username=email,password=password)
        if user is not None :
            if user.user_type=='TEAM_ED':
                auth.login(request,user,backend=None)
                return redirect('teams_eds_view_hrs')
            else:
                return redirect('students_login')
        else:
            return redirect('teams_eds_login')
    else:
        return render(request,'team_eds/login.html')


def add_student(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        if request.method == 'POST':
            user = User(fullname=request.POST['fname'],email=request.POST['email'],is_admin=True, user_type='VOLUNTEER')
            user.set_password(request.POST['pwd'])
            user.save()
            team=TeamEDS.objects.filter(head_user=request.user).first()
            team_match=TeamMatch(team_ed=team,student_users=user)
            team_match.save()
            return redirect('teams_eds_view_team')
        else:
            return render(request,'team_eds/add_student.html')
    else:
        return redirect('teams_eds_login')


def view_team(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        team=TeamEDS.objects.filter(head_user=request.user).first()
        students=TeamMatch.objects.all().filter(team_ed=team)
        return render(request,'team_eds/view_team.html',{"students":students})
    else:
        return redirect('teams_eds_login')


def view_hrs(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        team=TeamEDS.objects.filter(head_user=request.user).first()
        students=TeamMatch.objects.filter(team_ed=team).all()
        hrs=[]
        for student in students:
            hrs.append(Hr.objects.all().filter(added_by=student.student_users))
        return render(request,'team_eds/view_hrs.html',{"hrs":hrs})
    else:
        return redirect('teams_eds_login')

def teams_eds_view_allhrs(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        hrs=Hr.objects.all()
        return render(request,'team_eds/view_allhrs.html',{"hrs":hrs})
    else:
        return redirect('teams_eds_login')

def progress(request,email):
    if request.user.is_authenticated and check_team_ed(request.user):
        student=User.objects.filter(email=email).first()
        hr_prog=Hr.objects.filter(added_by=student).all()
        return render(request,'team_eds/progress.html',{"hr_prog":hr_prog})
    else:
        return redirect('teams_eds_login')


def changepassword(request):
    if request.user.is_authenticated and check_team_ed(request.user):
        if request.method == 'POST':
            oldpwd = request.POST['pwd']
            newpwd = request.POST['npwd']
            user = auth.authenticate(username=request.user.email,password=oldpwd)
            if user is not None:
                user=User.objects.filter(email=request.user.email).first()
                user.set_password(newpwd)
                user.save()
                auth.logout(request)
                return redirect('teams_eds_login')
            
            else:
                 return redirect('changepassword')
        else:
            return render(request,'team_eds/changepassword.html')
    else:
        return redirect('teams_eds_login')