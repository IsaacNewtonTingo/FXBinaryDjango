from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from FXBinaryProject import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.core.mail import send_mail

# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist. Please try some other username.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered")
            return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1, )
        myuser.first_name = fname
        myuser.last_name = "0"

        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(
            request, "Your Account has been created succesfully.Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Fx Binary Login!!"
        message = "Hi there! \n Welcome to Fx Binary! Ready to experience all the benefits of being financially independent? Before you head off to the races, make sure to verify your email address. \nCheck your mail box for a second email with a confirmation link."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Fx Binary Login!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            email = user.email
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html", {
                "fname": fname,
                "email": email,
            })
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    # messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


# Other pages--------------------------------------------------------------------

def account(request):

    return render(request, "authentication/account.html")


def terms(request):
    return render(request, "authentication/terms.html")


def getStarted(request):
    return render(request, "authentication/getStarted.html")


def deposit(request):

    if request.method == "POST":
        sender_email = request.POST['email']
        amount = request.POST['amount']

        # send mail
        send_mail(
            "Deposit alert by " + sender_email,  # subject
            sender_email + " has initiated a deposit of " + amount + \
            " USD. Please make the updates ASAP",  # message
            sender_email,  # from email
            ['info@azbinary.com'],  # to email
        )
        return render(request, "authentication/deposit.html", {
            'sender_email': sender_email,
            'amount_usd': amount,
        })
    else:
        return render(request, "authentication/deposit.html")


def withdraw(request):

    if request.method == "POST":
        sender_email = request.POST['btcEmail']
        amountUSD = request.POST['amountUSD']
        btcAddress = request.POST['btcAddress']

        # send mail
        send_mail(
            "Withdrawal request",
            sender_email + " wants to withdraw " + amountUSD +
            " USD Here is their BTC address : \n " + btcAddress,
            sender_email,
            ['info@azbinary.com'],
        )
        return render(request, "authentication/withdraw.html", {
            'sender_email': sender_email,
            'amount_usd': amountUSD,
        })

    else:
        return render(request, "authentication/withdraw.html")


def mpesaWithdrawal(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        mpesaEmail = request.POST['mpesaEmail']
        mpesaAmount = request.POST['mpesaAmount']

        # send mail
        send_mail(
            "M-Pesa withdrawal request",
            mpesaEmail + " wants to withdraw " + mpesaAmount +
            " USD. \n Here is their M-Pesa number : \n " + phone_number,
            mpesaEmail,
            ['info@azbinary.com'],
        )
        return render(request, "authentication/mpesaWithdrawal.html", {
            'mpesaEmail': mpesaEmail,
            'mpesaAmount': mpesaAmount,
        })

    else:
        return render(request, "authentication/mpesaWithdrawal.html")
