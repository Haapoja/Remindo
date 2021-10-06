from django.db import models
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy #this tool redirects the user from one part of the page to another
#login/register methods
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
 
# Create your views here.
class TermsConditions(TemplateView):
    template_name="base/terms.html"
    
#login view
class CustomLoginView(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True #prevents a logged in user from accessing this page
    #method for redirecting a user to the tasks page after login
    def get_success_url(self) -> str:
        return reverse_lazy("tasks")

#Register view
class RegisterPage(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        user = form.save()
        if user is not None: 
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(RegisterPage, self).get(*args, **kwargs)



#tasklist class inherits from ListView module
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks" #normally because of django, accessing this object would have to habben through the object_list variable, but renaming it makes the code easier to read
    #function that allows the user to only see their own tasks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        #send a get request, get the value from the search area defined in task_list.html
        search_input = self.request.GET.get("search-area") or ""
        #if there is search data
        if search_input:
            context["tasks"] = context["tasks"].filter(title__startswith=search_input)
        context["search_input"] = search_input
        return context


#allows the user the find detailed information about a task
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

#Create a task
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("tasks") #if task is created succesfully, redirect the user back to tasks
    #method that allows the user to create notes for himself/herself only
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    #restrict the user from seeing task unless he/she is authenticated
    

#view for updating the task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("tasks")

#Delete task view
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")