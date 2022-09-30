from django.shortcuts import redirect, render
from django.views.generic import TemplateView


# Login
class Login(TemplateView):
    template_name = "login.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
# Guest Login
class Guest(TemplateView):
    template_name = "guest.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# Register
class Register(TemplateView):
    template_name = "register.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
# Reset Password
class ResetPassword(TemplateView):
    template_name = "reset.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# Dashboard
class Dashboard(TemplateView):
    template_name = "dashboard.html"
    def get(self, request, *args, **kwargs):
        context = {"name": "Hanan"}
        return render(request, self.template_name, context)
    