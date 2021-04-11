from django.shortcuts import render
from .models import get_all_todo, add_todo, update_todo, delete_todo as delete
from django.views import View
from django.shortcuts import redirect


class TodoView(View):
    def get(self, request):
        todos = get_all_todo()
        return render(request, "todo_list.html", {'todos': todos})

    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        add_todo(title, description)
        return redirect('/')

def complete_todo(request, id):
    update_todo(id)
    return redirect('/')

def delete_todo(request, id):
    delete(id)
    return redirect('/')
