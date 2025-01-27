from django.shortcuts import redirect, render
from django.views import View
from .forms import UserRegisterForm
from django.contrib.auth import logout

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            print("Form is valid, redirecting to Home page")
            return redirect('index')
        else:
            print("Form is not valid")
        return render(request, 'users/register.html', {'form': form})
    
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'users/logout.html', {'message': 'You have been logged out successfully.'})
# Create your views here.
