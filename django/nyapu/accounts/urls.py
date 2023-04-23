from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
   path('edit_profile/', views.ProfileEditView.as_view(), name="edit_profile"),
   path('userlist/', views.UserListView.as_view(), name="userlist"),
]