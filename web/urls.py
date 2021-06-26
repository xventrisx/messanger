from django.urls import path
from .views import *

urlpatterns = [
    path('send_invitation_to_the_number/', send_invitation_to_the_number, name='controller_of_sending_a_message_to_the_phone_number'),
    path('page_invitations/', page_invite, name='url_of_the_page_for_sending_sms_with_a_code'),
    path('page_chennel/<int:id>/', view_channel),
    path('page_create_newe_channel/', view_create_newe_channel, name='views_create_newe_channel'),
    path('page_create_newe_group/', view_create_newe_group, name='views_create_newe_group'),
    path('create_channel/', create_channel),
    path('create_group/', create_group),
    path('checking_user/', checking_user),
    path('phone_confirmation/', phone_confirmation, name=''),
    path('web_authorization/', controller_authorization, name='authentication_controller_url'),
    path('view_home_page/', view_home_page, name='url_controller_displaying_the_main_page'),
    path('page_login/', page_login, name='url_to_enter_phone_number'),
    path('page_password/', page_password, name='url_to_enter_password_user'),
    path('password_with_sms/', password_with_sms, name='url_phone_number_verification'),
    path('page_my_contact/', page_my_contact, name='url_of_the_user_s_contact_list_page'),
    path('chat_with_user/<int:id>/', page_chat_with_user),
    path('send_message/', send_message),
    path('exit/', log_out, name='session_user_logout'),
]