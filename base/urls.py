from django.urls import path
from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage, TermsConditions
from django.contrib.auth.views import LogoutView
#handles urls
urlpatterns = [
    path("terms/", TermsConditions.as_view(), name="terms"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
    #empty string=base.
    path("", TaskList.as_view(), name="tasks"),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("create-task/", TaskCreate.as_view(), name="create-task"),
    path("edit-task/<int:pk>/", TaskUpdate.as_view(), name="edit-task"),
    path("delete-task/<int:pk>/", DeleteView.as_view(), name="delete-task"),
]