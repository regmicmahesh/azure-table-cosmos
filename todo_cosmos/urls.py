from django.urls import path
from . import views

app_name = "todo"

urlpatterns= [
    path('', views.TodoView.as_view(), name='home'),
    path('completed/<str:id>', views.complete_todo, name='complete'),
    path('delete/<str:id>', views.delete_todo, name='delete')
]