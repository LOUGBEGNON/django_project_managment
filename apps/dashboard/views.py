from lib2to3.fixes.fix_input import context

from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import *
from apps.dashboard.models import Project
import django.contrib.messages as messages
import plotly.express as px


# Create your views here.

@login_required(login_url="/login_auth/")
def index(request):
    print(request.user)
    projects = Project.objects.all().order_by('-creation_date')[:3]
    print(projects)

    if request.method == "POST":
        # Adding forms
        formProject = AddProjectForm(request.POST)
        if formProject.is_valid():
            # category = request.POST.get("category")
            # recurrent = request.POST.get("recurrent")
            project = formProject.save(commit=False)
            project.author = request.user
            description = formProject.cleaned_data.get("text")
            # content.location = request.POST.get("location")
            # content.start_date_time = datetime.strptime(
            #     request.POST.get("start_date_time"), "%Y-%m-%d %H:%M"
            # )
            # content.end_date_time = datetime.strptime(
            #     request.POST.get("end_date_time"), "%Y-%m-%d %H:%M"
            # )
            # content.category = int(category)
            # content.recurrent = int(recurrent)
            # content.text = text
            # content.title = get_utf8_standardized_string(
            #     remove_html_tags(text).strip().split(".")[0]
            # )
            # content.status = 2
            # content.last_update = datetime.now()
            #
            # content.save()
            # Without this next line the tags won't be saved.
            project.save()
            messages.success(
                request,
                f'The project "{project.name}" has been successfully published.',
            )
            return redirect(
                reverse(
                    "view_project",
                    kwargs={
                        "id": project.id,
                    },
                )
            )
            # return redirect(
            #    "view_community",
            #    municipality_slug=request.user.individual.municipality_slug,
            # )
        else:
            print(formProject.errors)
            messages.error(request, "The project form is not valid")
    else:
        # Adding forms
        formProject = AddProjectForm()

    # Adding forms
    # formProject = AddProjectForm()
    context = {
        'user': request.user,
        'projects': projects,
        "formProject": formProject,
    }
    return render(request, "dashboard/index.html", context)


@login_required(login_url="/login_auth/")
def view_project(request, id):
    try:
        project = Project.objects.get(pk=id)

        if project.status == '0':
            project.status = 'CREATED'
        if project.status == '1':
            project.status = 'IN PROGRESS'
        if project.status == '2':
            project.status = "PAUSED"
        if project.status == '3':
            project.status = "COMPLETED"


        tasks = Task.objects.filter(project=project)
        tasks_for_tables = tasks

        for task in tasks_for_tables:
            if task.status == '0':
                task.status = 'CREATED'
            if task.status == '1':
                task.status = 'IN PROGRESS'
            if task.status == '2':
                task.status = "PAUSED"
            if task.status == '3':
                task.status = "COMPLETED"
        print(tasks)
        print(project)
        print(project.description)

        # task_data = [
        #     {"Task": "Research", "Start": "2024-09-01", "Finish": "2024-09-10"},
        #     {"Task": "Planning", "Start": "2024-09-11", "Finish": "2024-09-15"},
        #     {"Task": "Development", "Start": "2024-09-16", "Finish": "2024-09-25"},
        #     {"Task": "Testing", "Start": "2024-09-26", "Finish": "2024-09-30"},
        #     {"Task": "Deployment", "Start": "2024-10-01", "Finish": "2024-10-05"}
        # ]

        tasks_for_diagram = Task.objects.filter(project = id)
        task_data = [
            {"Task": task.name, "Start": task.start_date, "Finish": task.end_date}
            for task in tasks_for_diagram
        ]

        fig = px.timeline(task_data, x_start="Start", x_end="Finish", y="Task", title="Diagramme de Gantt")
        fig.update_yaxes(categoryorder="total ascending")  # Ordonner les tâches par dates

        chart_html = fig.to_html()

        if request.method == "POST":
            form = AddTaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.project = project
                task.author = request.user
                task.save()
                return redirect(
                    reverse(
                        "view_project",
                        kwargs={
                            "id": project.id,
                        },
                    )
                )
            else:
                print(form.errors)
        else:
            form = AddTaskForm()

        context = {
            "project": project,
            "form": form,
            "tasks": tasks,
            "tasks_for_tables": tasks_for_tables,
            "chart_html": chart_html,
        }
        return render(request, "dashboard/view_project.html", context)
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def start_task(request, id):
    try:
        task = Task.objects.get(pk=id)
        print(task.status)
        project = Project.objects.get(project=task)
        task.start()
        print(task.status)
        return redirect(
            reverse(
                "view_project",
                kwargs={
                    "id": project.id,
                },
            )
        )
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def complete_task(request, id):
    try:
        task = Task.objects.get(pk=id)
        project = Project.objects.get(project=task)
        task.pause()
        return redirect(
            reverse(
                "view_project",
                kwargs={
                    "id": project.id,
                },
            )
        )
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def pause_task(request, id):
    try:
        task = Task.objects.get(pk=id)
        project = Project.objects.get(project=task)
        task.pause()
        return redirect(
            reverse(
                "view_project",
                kwargs={
                    "id": project.id,
                },
            )
        )
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def complete_task(request, id):
    try:
        task = Task.objects.get(pk=id)
        project = Project.objects.get(project=task)
        task.complete()
        return redirect(
            reverse(
                "view_project",
                kwargs={
                    "id": project.id,
                },
            )
        )
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


def task_gantt_chart(request):
    tasks = Task.objects.all()
    # task_data = [
    #     {"Task": task.name, "Start": task.start_date, "Finish": task.end_date}
    #     for task in tasks
    # ]

    task_data = [
        {"Task": "Research", "Start": "2024-09-01", "Finish": "2024-09-10"},
        {"Task": "Planning", "Start": "2024-09-11", "Finish": "2024-09-15"},
        {"Task": "Development", "Start": "2024-09-16", "Finish": "2024-09-25"},
        {"Task": "Testing", "Start": "2024-09-26", "Finish": "2024-09-30"},
        {"Task": "Deployment", "Start": "2024-10-01", "Finish": "2024-10-05"}
    ]

    fig = px.timeline(task_data, x_start="Start", x_end="Finish", y="Task", title="Diagramme de Gantt des Tâches")
    fig.update_yaxes(categoryorder="total ascending")  # Ordonner les tâches par dates

    chart_html = fig.to_html()

    return render(request, 'dashboard/gantt_chart.html', {'chart_html': chart_html})


def anychart_gantt(request):
    tasks = Task.objects.all()
    task_data = [
        {"Task": "Research", "Start": "2024-09-01", "Finish": "2024-09-10"},
        {"Task": "Planning", "Start": "2024-09-11", "Finish": "2024-09-15"},
        {"Task": "Development", "Start": "2024-09-16", "Finish": "2024-09-25"},
        {"Task": "Testing", "Start": "2024-09-26", "Finish": "2024-09-30"},
        {"Task": "Deployment", "Start": "2024-10-01", "Finish": "2024-10-05"}
    ]
    return render(request, 'dashboard/anychart_gantt.html', {'task_data': task_data})


def task_gantt_chart_matplotlib(request):
    tasks = Task.objects.all()
    # task_data = [
    #     {"Task": task.name, "Start": task.start_date, "Finish": task.end_date}
    #     for task in tasks
    # ]

    task_data = [
        {"Task": "Research", "Start": "2024-09-01", "Finish": "2024-09-10"},
        {"Task": "Planning", "Start": "2024-09-11", "Finish": "2024-09-15"},
        {"Task": "Development", "Start": "2024-09-16", "Finish": "2024-09-25"},
        {"Task": "Testing", "Start": "2024-09-26", "Finish": "2024-09-30"},
        {"Task": "Deployment", "Start": "2024-10-01", "Finish": "2024-10-05"}
    ]

    fig = px.timeline(task_data, x_start="Start", x_end="Finish", y="Task", title="Diagramme de Gantt des Tâches")
    fig.update_yaxes(categoryorder="total ascending")  # Ordonner les tâches par dates

    chart_html = fig.to_html()

    return render(request, 'dashboard/gantt_chart.html', {'chart_html': chart_html})



@login_required(login_url="/login_auth/")
def projects(request):
    projects = Project.objects.filter(author=request.user)
    for project in projects:
        pass
        # project.author =

    if request.method == "POST":
        # Adding forms
        formProject = AddProjectForm(request.POST)
        if formProject.is_valid():
            project = formProject.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(
                request,
                f'The project "{project.name}" has been successfully published.',
            )
            return redirect(
                reverse(
                    "view_project",
                    kwargs={
                        "id": project.id,
                    },
                )
            )
            # return redirect(
            #    "view_community",
            #    municipality_slug=request.user.individual.municipality_slug,
            # )
        else:
            print(formProject.errors)
            messages.error(request, "The project form is not valid")
    else:
        # Adding forms
        formProject = AddProjectForm()

    context = {
        "projects": projects,
        "formProject": formProject,
    }
    return render(request, "dashboard/projects.html", context)


def billing(request):
  return render(request, 'dashboard/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'dashboard/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'dashboard/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'dashboard/rtl.html', { 'segment': 'rtl' })

@login_required(login_url="/login_auth/")
def profile(request):
    if request.user.role == 1:
        request.user.role = 'USER'
    elif request.user.role == 2:
        request.user.role = 'MEMBER'
    elif request.user.role == 3:
        request.user.role = 'STAFF'
    elif request.user.role == 4:
        request.user.role = 'MANAGER' 
    elif request.user.role == 5:
        request.user.role = 'ADMIN' 
    return render(request, 'dashboard/profile.html', { 'segment': 'profile' })


