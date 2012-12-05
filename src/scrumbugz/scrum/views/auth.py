from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate

from scrum.forms.auth import LoginForm

class LoginView(FormView):
    template_name = "scrum/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)

        next = self.request.GET.get('next') or '/'
        return redirect(next)
