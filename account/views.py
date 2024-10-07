from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import Login_Form, AddNewUser, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import Custom_User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


def LogIn(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = Login_Form()
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            user = form.get_user()
            print('asdflkj', user)

            login(request, user)
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'account/login.html', context)


def Logout(request):
    logout(request)
    return redirect('login')


@login_required
def addNewUser(request):
    if request.method == 'POST':
        form = AddNewUser(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = form.save()
            user.set_password(password)
            if user.user_type == 'Admin':
                user.is_staff = True
                user.is_superuser = True
            user.save()
            return redirect('member_list')
        else:
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = AddNewUser()
        context = {'form': form}
    return render(request, 'account/add_new_user.html', context)


@login_required
def my_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = get_object_or_404(Custom_User, username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.save()
        current_password = request.user.password

        if old_password and new_password and confirm_new_password:
            old_password_check = check_password(old_password, current_password)
            if old_password_check:
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    user.save()
                    messages.warning(request, "Password Change Successfully!")
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    messages.warning(
                        request, "New password & confirm new password is doesn't match!")
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.warning(request, 'Old Password is not currect!')
                return redirect(request.META['HTTP_REFERER'])
        else:
            messages.warning(request, "Profile Details Update Successfully!")
            return redirect(request.META['HTTP_REFERER'])

    return render(request, 'account/my_profile.html')


@login_required
def member_list(request):
    member = Custom_User.objects.all()
    context = {'member': member}
    return render(request, 'account/member_list.html', context)

class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Custom_User
    template_name = 'account/user_confirm_delete.html'
    success_url = reverse_lazy('member_list')

@login_required
def member_view(request, id):
    member = get_object_or_404(Custom_User, id=id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=member)
        print(form)
        if form.is_valid():
            member = form.save(commit=False)
            
            # Check if the password was changed
            new_password = form.cleaned_data.get('password')
            if new_password:
                member.set_password(new_password)
                update_session_auth_hash(request, member)  # To avoid logging out the user
            
            member.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, f'{form.errors}')
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = UserProfileForm(instance=member)
    return render(request, 'account/member_view.html', {'form': form, 'member': member})




