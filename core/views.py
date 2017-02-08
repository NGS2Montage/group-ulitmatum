from annoying.decorators import render_to

from .models import Game

# Auth related
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail


@render_to('state-mismatch.html')
@login_required
def state_mismatch(request):
    context = {
        "game": Game.objects.get_current_game()
    }
    # fill in context dict with stuff to pass to template as needed
    return context


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        password = request.POST['password']
        user.set_password(password)
        user.save()
        return render(request, 'account/change_password.html', {'successMessage': "success"})
    return render(request, 'account/change_password.html', {})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/account/')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except Exception, e:
            return render(request, 'account/login.html', {'usernameError': "*Username doesn't exist"})

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/account/')
            else:
                return render(request, 'account/login.html', {
                    'inActiveError': 'Your account is still not activated. Please contact Admin at replace@email.me to activate your account.'})
        else:
            return render(request, 'account/login.html',
                          {'passwordError': "*Password doesn't match. Please try again."})
    return render(request, 'account/login.html', {})


def create_account(request):
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        formData = {'firstName': firstName, 'lastName': lastName, 'email': email, 'username': username}
        try:
            user = User.objects.get(email=email)
            return render(request, 'account/create_account.html',
                          {'emailError': "Email Error", 'formData': formData})
        except Exception, e:
            pass

        try:
            user = User.objects.get(username=username)
            return render(request, 'account/create_account.html',
                          {'userNameError': "Username Error", 'formData': formData})
        except Exception, e:
            pass

        user = User(username=username, email=email, first_name=firstName, \
                    last_name=lastName, is_active=False, password=password)
        user.save()
        user.set_password(user.password)
        user.save()
        body = '''Hi,<br/><br/>

        A request for the creation of a new account has been received. Mentioned below are the details:<br/>
        <ul>
            <li><b>Username:</b> %s</li>
            <li><b>Email:</b> %s</li>
            <li><b>Name:</b> %s %s</li>
        </ul><br/>
        Please take the required action by visiting the site admin.<br/><br/>
        Regards,<br/>
        The EMBERS AutoGSR System<br/>''' % (username, email, firstName, lastName)

        emailSendError = '''There was a problem creating your account.<br/>
                        Please send an email to system admin at <u>replace@email.me</u><br/>
                        '''
        try:
            send_mail(subject="User Account Creation Request", html_message=body,
                      recipient_list=['recipient@list.me'],
                      message="", from_email='replace@email.me')
        except Exception, e:
            return render(request, 'account/create_account.html', {'emailSendError': emailSendError})

        successMessage = ''' Your account has been successfully created but is <u>NOT</u> activated yet.<br/><br/>
                             Please wait for the system admin to activate your account.<br/>
                             If required, you can reach the system admin at <u>replace@email.me</u>'''
        return render(request, 'account/create_account.html', {'successMessage': successMessage})
    return render(request, 'account/create_account.html', {})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except Exception, e:
            return render(request, 'account/forgot_password.html', {'emailError': "email Error", "formData": email})

        emailBody = '''Hi,<br/><br/>

        The following user has made a request to reset the account password:<br/>
        <ul>
            <li><b>Username:</b> %s</li>
            <li><b>Email:</b> %s</li>
        </ul></br/>
        Please take the required action by visiting the site admin.<br/><br/>
        Regards,<br/>
        The EMBERS AutoGSR System''' % (user.username, email)

        emailSendError = '''There was a problem resetting your account.<br/>
                        Please send an email to system admin at <u>replace@email.me</u><br/>
                        '''
        try:
            send_mail(subject="Password Reset Request", html_message=emailBody,
                      recipient_list=['recipient@list.me'],
                      message="", from_email='replace@email.me')
        except Exception, e:
            return render(request, 'account/forgot_password.html', {'emailSendError': emailSendError})

        successMessage = ''' Your password reset request has been received.<br/><br/>
                             Please wait for the system admin to reset your password.<br/>
                             If required, you can reach the system admin at <u>replace@email.me</u>'''
        return render(request, 'account/forgot_password.html', {'successMessage': successMessage})

    return render(request, 'account/forgot_password.html', {})
