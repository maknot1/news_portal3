from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

@login_required
def upgrade_me(request):
    premium, created = Group.objects.get_or_create(name='premium')

    request.user.groups.clear()
    request.user.groups.add(premium)

    return redirect("/")

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profile_edit.html'
    success_url = '/'

    def get_object(self):
        return self.request.user