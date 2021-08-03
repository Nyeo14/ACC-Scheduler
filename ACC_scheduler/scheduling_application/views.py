
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import SeniorForm
from .models import Senior, Volunteer, Appointment
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail



def home(response):
    """View for the home page"""
    return render(response, "scheduling_application/home.html", {})


def login(request):
    """View for the login page"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')                 # TEMPORARY
    return render(request, 'scheduling_application/login.html', {})


# uses Django's built-in UserRegisterForm
def register(request):
    """View for the registration page"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')         # resume tutorial for message display on main page
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'scheduling_application/register.html', {'form': form})


# Django messages may make this obsolete.
def success(response):
    """View for the email sending success page"""
    return render(response, "scheduling_application/success.html", {})


def appointment(request):
    """View for the page where users can schedule an appointment.
       Shows current seniors, volunteers, and appointments.
       Allows users to choose a senior and day then continue."""
    seniors_list = Senior.objects.all()
    volunteers_list = Volunteer.objects.all()
    appointments_list = Appointment.objects.all()

    context = {
        'seniors_list': seniors_list,
        'volunteers_list': volunteers_list,
        'appointments_list': appointments_list
    }

    # Handle scheduling appointment
    if request.method == 'POST':
        senior = request.POST['senior']
        day = request.POST['day']
        potential_list = Volunteer.objects.filter(day=day).values()         # get only volunteers' first and last name
        context = {
            'seniors_list': seniors_list,
            'volunteers_list': volunteers_list,
            'potential_list': potential_list,
            'appointments_list': appointments_list
        }
        request.session['potential_list'] = list(potential_list)
        return redirect('confirm_v')
    return render(request, 'scheduling_application/appointment.html', context)



def confirm_v(request):
    """View for page to confirm which volunteers to send emails to."""
    potential_list = request.session['potential_list']
    print(potential_list)
    available_volunteer_list = []
    for i in potential_list:
        available_volunteer_list.append(i['first_name'] + " " + i['last_name'])

    context = {
        'available_volunteer_list': available_volunteer_list
    }
    if request.method == 'POST':
        selected_volunteers = request.POST.getlist('volunteer')
        print(selected_volunteers)
        email_subject = 'TEMPORARY SUBJECT'
        email_message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.'
        from_email = 'acc.scheduler.care@gmail.com'
        to_email = [i['email'] for i in potential_list if potential_list[0]['first_name'] in selected_volunteers]
        send_mail(email_subject, email_message, from_email, to_email)
        print(to_email)
        # RETURN MESSAGE "EMAILS SUCCESSFULLY SENT"
    print("available_volunteer_list", available_volunteer_list)
    return render(request, 'scheduling_application/confirm_v.html', context)


def index(request):
    """View for index page (home page when logged in)"""
    return render(request, 'scheduling_application/index.html', {})


def logout(request):
    """View for logging out"""
    auth.logout(request)
    return redirect('home')


def view_seniors(request):
    """View for the seniors page (table of all the seniors in the database)"""
    seniors = Senior.objects.all()
    context = {
        'seniors': seniors,
    }
    return render(request, 'scheduling_application/view_seniors.html', context)

def add_senior(request):
    """View for adding senior page"""
    form = SeniorForm()
    if request.method == 'POST':
        form = SeniorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('view_seniors')
    context = {
        'form': form
    }
    return render(request, 'scheduling_application/add_senior.html', context)

def senior_page(request, last_name):
    """View for senior profile page"""
    senior = Senior.objects.get(last_name=last_name)
    if request.method == 'POST':
        senior.delete()
        return redirect('view_seniors')
    context = {
        'senior': senior,
    }
    return render(request, 'scheduling_application/senior_page.html', context)

def view_volunteers(request):
    """View for the volunteers page (table of all the volunteers in the database)"""
    volunteers = Volunteer.objects.all()
    context = {
        'volunteers': volunteers,
    }
    return render(request, 'scheduling_application/view_volunteers.html', context)