from django.views.generic import ListView, DeleteView, UpdateView, View, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import Login_Form, AddNewUser, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Custom_User
from django.db.models import Q
import os

class LogInView(FormView):
    template_name = 'account/login.html'
    form_class = Login_Form
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)  # Log in the user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LogOutView(LoginRequiredMixin, View):
    """Handle user logout."""
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class AddNewUserView(LoginRequiredMixin, CreateView):
    model = Custom_User
    form_class = AddNewUser
    template_name = 'account/add_new_user.html'
    success_url = reverse_lazy('member_list')

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        user = form.save(commit=False)
        user.set_password(password)  # Set the password
        
        if user.user_type == 'Admin':
            user.is_staff = True
            user.is_superuser = True
        
        user.save()
        messages.success(self.request, 'New user added successfully!')  # Add a success message
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

class MyProfileView(LoginRequiredMixin, View):
    template_name = 'account/my_profile.html'

    def get(self, request, *args, **kwargs):
        """Render the profile page."""
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        profile_picture = request.FILES.get('profile_picture')
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = get_object_or_404(Custom_User, username=username)
        
        if profile_picture:
            if user.profile_picture:
                os.remove(user.profile_picture.path)
            user.profile_picture = profile_picture
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.save()
        
        if old_password and new_password and confirm_new_password:
            old_password_check = user.check_password(old_password)
            if old_password_check:
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Avoid logging out the user
                    messages.success(request, "Password changed successfully!")
                else:
                    messages.warning(request, "New password and confirmation do not match!")
            else:
                messages.warning(request, 'Old password is incorrect!')
        else:
            messages.success(request, "Profile details updated successfully!")

        return redirect(request.META['HTTP_REFERER'])

class MemberListView(LoginRequiredMixin, ListView):
    model = Custom_User
    template_name = 'account/member_list.html'
    context_object_name = 'member'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(username__icontains=search_query) |
                Q(user_type__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        return queryset

class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Custom_User
    template_name = 'account/user_confirm_delete.html'
    success_url = reverse_lazy('member_list')

class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Custom_User
    form_class = UserProfileForm
    template_name = 'account/member_view.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Custom_User, id=self.kwargs['id'])
    
    def form_valid(self, form):
        member = form.save(commit=False)
        new_password = form.cleaned_data.get('password')
        if new_password:
            member.set_password(new_password)
            update_session_auth_hash(self.request, member)  # Avoid logging out the user
        member.save()
        messages.success(self.request, 'Your profile was updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{form.errors}')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']


