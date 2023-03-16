from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from todo.forms import TaskForm
from todo.models import Task


def index(req: HttpRequest) -> HttpResponse:
    template = 'todo/index.html'

    tasks = Task.objects.all()

    context = {
        'tasks': tasks,
    }

    return render(req, template, context)


@login_required
def create_task(req: HttpRequest) -> HttpResponse:
    form = TaskForm(req.POST or None, files=req.FILES or None)

    template = 'todo/create_task.html'

    context = {
        'form': form,
        'action_url': 'todo:create_task'
    }

    if not req.method == 'POST' or not form.is_valid():
        return render(req, template, context)

    task = form.save(commit=False)
    # task.created_by = req.user
    task.save()
    return redirect('todo:index')
