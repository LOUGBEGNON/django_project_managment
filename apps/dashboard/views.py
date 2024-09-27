from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import *
from apps.dashboard.models import Project
import django.contrib.messages as messages



# Create your views here.

@login_required(login_url="/login_auth/")
def index(request):
    print(request.user)
    projects = Project.objects.all().order_by('-creation_date')[:3]
    print(projects)
    print("ndfjkbdgvbdjfvjdfnv")

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


def view_project(request, id):
    try:
        project = Project.objects.get(pk=id)
        print(project)
        print(project.description)

        # if (post.user != request.user) and (
        #     post.status is not settings.PUBLISHED_STATUS
        # ):
        #     messages.error(request, "You are not allowed to view this post")
        #     return redirect(
        #         "view_community",
        #         municipality_slug=request.user.individual.municipality_slug,
        #     )

        context = {
            "project": project,
        }
        return render(request, "dashboard/project/view_project.html", context)
    except Exception:
        return redirect(
            "404",
        )


def projects(request):
    projects = Project.objects.filter(author=request.user)
    context = {
        "projects": projects
    }
    return render(request, "dashboard/project/projects.html", context)


def billing(request):
  return render(request, 'dashboard/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'dashboard/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'dashboard/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'dashboard/rtl.html', { 'segment': 'rtl' })

def profile(request):
  return render(request, 'dashboard/profile.html', { 'segment': 'profile' })


