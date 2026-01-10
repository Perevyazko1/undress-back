from django.urls import path
from .views import check_user,create_user,add_tokens,spend_tokens,get_tokens,set_callback_data,get_callback_data

urlpatterns = [
    path('check-user/', check_user),
    path('create-user/', create_user),
    path('add-tokens/', add_tokens),
    path('spend-tokens/', spend_tokens),
    path('get-tokens/', get_tokens),
    path('set-callback-data/', set_callback_data),
    path('get-callback-data/', get_callback_data),
]