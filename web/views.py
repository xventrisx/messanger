import typing
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from authentication.models.user import User
from authentication.models.password import Ticket
from authentication.services import *
from .form import *
from services.services import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password, is_password_usable, check_password


def log_out(request):
    '''
    User logout controller
    '''
    logout(request)
    return redirect('/web/page_login')


def page_login(request):
    '''
    The controller submits a form to enter the phone number.
    '''
    context = {
        'phone_form': PhoneForm(),
    }
    return render(request, 'login.html', context)


def page_password(request):
    '''
    Based on the input data, the controller sends the forum to enter the user's password,
    or sends a message to the phone number with a unique password for further registration
    of the number in the database.
    '''
    if User.objects.filter(phone=int(request.POST['phone'])).exists():
        context = {
            'form_password': PasswordForm(),
            'phone': request.POST['phone'],
        }
        return render(request, 'password enter.html', context)
    else:
        context = {
            'phone': request.POST['phone'],
        }
        return render(request, 'registration_offer_page.html', context)


def password_with_sms(request):
    '''
    The controller sends a form to enter the password received via SMS
    '''
    context = {
        'form_password': PasswordForm(),
    }
    return render(request, 'phone password.html', context)


def phone_confirmation(request):
    '''
    The controller verifies the existence of the invitation for registration,
    otherwise, notifies the user that the invitation is invalid.
    '''
    try:
        Ticket.objects.get(password=request.POST['password'])
        context = {
            'password_sms': request.POST['password'],
            'checkin_form': CheckinForm(),
        }
        return render(request, 'create user.html', context)
    except Ticket.DoesNotExist:
        return render(request, 'invalid password sms.html')


def checking_user(request):
    if create_user(data=request.POST) != None:
        return render(request, 'sentnotification.html')
    else:
        return render(request, 'not this way.html')


@login_required(login_url='/web/page_login/')
def view_home_page(request):
    chat = ChatManager(request.user)
    dialog = chat.get_dialogs_user()
    group = chat.get_gruops_user()
    channels = chat.get_channels_user()
    context = dict(
        dialog=dialog,
        group=group,
        channels=channels
    )
    return render(request, 'home page.html', context)


def controller_authorization(request):
    '''
    The controller redirects the user to the required page depending on the result of the function web_authorization
    '''

    result = web_authorization(request.POST)
    if result is None:

        '''
        If a user with the specified phone number is not found,
        the user will be redirected to the corresponding page with a notification about it.
        '''

        return render(request, 'phone_number_not_found.html')

    elif not result:

        '''
        If the user entered an incorrect password, he will be informed about it
        '''

        return render(request, 'invalid_password.html')

    elif isinstance(result, User):
        login(request, result)
        return redirect('/web/view_home_page')


def view_create_newe_group(request):
    '''
    The controller is responsible for displaying a list of all contacts,
    and submitting a form to get the name of a new group.
    '''

    contacts = get_contact_for_user(request.user)
    context = {
        'form_add_group': CreateFormGroup(),
        'contacts': contacts,
    }
    return render(request, 'page_create_group.html', context)


def create_group(request):
    group = add_group(request)
    return redirect('/web/view_home_page')


@login_required(login_url='/web/page_login/')
def page_my_contact(request):
    '''
    This controller displays the page with the user's contacts. If there are no contacts,
    the user is invited to invite the person by phone number.
    '''
    contacts = get_contact_for_user(request.user)
    if contacts is not None:
        ''' The condition checks whether the user has a contact '''
        context = {
            'contacts': contacts,
        }
        return render(request, 'my contact.html', context)
    else:
        return redirect('/web/page_invitations/')


@login_required(login_url='/web/page_login/')
def page_invite(request):
    '''
    Controller of displaying a page with a proposal to invite a user by phone number.
    '''
    context = {
        'form_phone': PhoneForm()
    }
    return render(request, 'invite user.html', context)


def send_invitation_to_the_number(request):
    '''
    This controller starts the service of sending a message to a phone number. If the user is logged in,
    he is transferred to the main page, if not, then he is transferred to the page for entering the phone number
    to log into the system.
    '''
    if request.user.is_authenticated:
        checkin(request.POST)
        return redirect('/web/view_home_page')
    else:
        checkin(request.POST)
        return redirect('/web/password_with_sms')


def page_chat_with_user(request, id: typing.Optional[int]):
    chat_manager = ChatManager(request.user, companion_id=id)
    result = chat_manager.get_or_create_dialog_with_user()
    messag_manager = MessagManager(
        request.user,
    )
    for x in result['messages']:
        read = messag_manager.set_who_read(x)
    context = {
        'result': result,
        'messegesform': MessageForm(),
    }
    return render(request, 'chat with user.html', context)


def send_message(request):
    messag_manager = MessagManager(
        request.user,
        request.POST['text_message'],
        request.POST['dialog_id'],
    )
    message = messag_manager.create_message()
    read = messag_manager.set_who_read(message)
    return redirect('/web/chat_with_user/{}'.format(request.POST['companion_id']))


def view_create_newe_channel(request):
    contacts = get_contact_for_user(request.user)
    if contacts != None:
        context = {
            'form_name_chanel': CreateFormGroup(),
            'contacts': contacts,
        }
        return render(request, 'page create chanel.html', context)
    else:
        context = {
            'form_name_chanel': form_name_chanel,
        }
        return render(request, 'page create chanel.html', context)


def view_channel(request, id):
    manager = ChatManager(request.user)
    result = manager.get_channel(id=id)
    manager_messag = MessagManager(request.user, chat=result)
    messages = manager_messag.get_messages()
    context = {
        'channel': result,
        'messages': messages,
    }
    return render(request, 'page chanel.html', context)


def create_channel(request):
    manager = ChatManager(request.user)
    result = manager.create_channel(request.POST)
    return redirect('/web/page_chennel/{}'.format(result.id))
