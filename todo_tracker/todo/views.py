from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from todo.forms import TaskForm
from todo.models import Task


def index(req: HttpRequest) -> HttpResponse:
    if not req.user.is_authenticated:
        return redirect('users:login')
    user = req.user
    template = 'todo/index.html'
    tasks = Task.objects.filter(created_by=user)
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
        # 'action_url': {
        #     'url': 'todo:create_task',
        # },
    }

    if not req.method == 'POST' or not form.is_valid():
        return render(req, template, context)

    task = form.save(commit=False)
    task.created_by = req.user
    task.save()
    return redirect('todo:index')


@login_required
def update_task(req: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(instance=task)
    template = 'todo/update_task.html'
    context = {
        'form': form,
        'is_edit': True,
        'task_id': task_id,
    }

    if not req.method == 'POST':
        return render(req, template, context)

    if req.method == 'POST':
        form = TaskForm(req.POST or None, files=req.FILES, instance=task)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = req.user
            form.save()
            return redirect('todo:index')
        context['form'] = form
        return render(req, template, context)


@login_required
def delete_task(req:HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=task_id)
    if req.user == task.created_by:
        task.delete()
    return redirect('todo:index')
