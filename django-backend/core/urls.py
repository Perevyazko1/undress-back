from django.urls import path
from .views import check_user,create_user,add_tokens,spend_tokens

urlpatterns = [
    path('check-user/', check_user),
    path('create-user/', create_user),
    path('add-tokens/', add_tokens),
    path('spend-tokens/', spend_tokens),
]