from django.urls import path
from .views import upgrade_me, ProfileEditView

urlpatterns = [
    path("upgrade/", upgrade_me, name="upgrade"),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
]