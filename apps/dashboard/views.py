from datetime import datetime
from lib2to3.fixes.fix_input import context

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.transaction import commit
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import *
from apps.dashboard.models import Project
import django.contrib.messages as messages
import plotly.express as px

from ..authentication.forms import UpdateCompanyForm
from ..utils import generate_slug
from django.conf import settings
from django.db.models import Q


@login_required(login_url="/login_auth/")
def index(request):
    print(request.user.get_role)
    if request.user.role == request.user.MANAGER and not request.user.company:
        return redirect('create_company')
    if not request.user.is_active:
        return redirect("inactive_account")
    company = Company.objects.get(pk=request.user.company.id)

    projects = Project.objects.filter(author=request.user).order_by('-creation_date')[:3]
    if request.method == "POST":
        formProject = AddProjectForm(request.POST)
        if formProject.is_valid():
            # category = request.POST.get("category")
            # recurrent = request.POST.get("recurrent")
            project = formProject.save(commit=False)
            project.author = request.user
            project.slug = generate_slug(project.name, 10)
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
            # Faire l'envoi de mail à la création de projet
            send_mail_create_project_author(request, project)
            if project.responsible:
                send_mail_create_project_responsible(request, project)
            messages.success(
                request,
                f'The project "{project.name}" has been successfully created.',
            )
            return redirect(
                reverse(
                    "view_project",
                    kwargs={
                        "id": project.id,
                    },
                )
            )
        else:
            print(formProject.errors)
            messages.error(request, "The project form is not valid")
    else:
        formProject = AddProjectForm()
        formInvite = InviteForm()
    context = {
        'segment': 'index',
        "company": company,
        'user': request.user,
        'projects': projects,
        "formProject": formProject,
        "formInvite": formInvite,
    }
    return render(request, "dashboard/index.html", context)

@login_required(login_url="/login_auth/")
def create_company(request):
    maintenant = datetime.now()
    date_heure = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    print(date_heure)
    form = AddCompanyForm()

    if request.method == 'POST':
        form = AddCompanyForm(request.POST)
        # context = {'form':form}
        if form.is_valid():
            company = form.save(commit=False)
            # social_name = company.cleaned_data.get("social_name")
            # name = company.cleaned_data.get("name")
            # email = company.cleaned_data.get("email")
            # address = company.cleaned_data.get("address")
            company.responsible = request.user
            company.save()

            request.user.company = company
            request.user.save()

            messages.success(request, f"Company created {company.name}")
            created = True
            # form = CompanyRegistrationForm()
            # context = {
            #     'created' : created,
            #     'form' : form,
            #            }
            # return render(request, 'register/new_company.html', context)
            return redirect("home")
        else:
            print(form.errors)
            return render(request, 'register/new_company.html')
    # else:
    context = {
        'form': form,
        "date": date_heure
    }
    return render(request, 'dashboard/home_new_company.html', context)


def send_mail_app(request):
    maintenant = datetime.now()
    date_heure = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    form = SendMailForm()

    if request.method == 'POST':
        form = SendMailForm(request.POST)
        # context = {'form':form}
        if form.is_valid():
            # mail = form.save(commit=False)
            subject = request.POST.get("subject")
            message = request.POST.get("message")
            to_email = request.POST.get("email")

            from_email = settings.DEFAULT_FROM_EMAIL

            try:
                logger.info(f"Send email for {to_email}")

                send_mail(
                    subject,
                    message,
                    from_email,
                    [to_email,],
                    fail_silently=False,
                )
                messages.success(request, f"Mail sent")

                referer = request.META.get('HTTP_REFERER')
                if referer:
                    return redirect(referer)
                else:
                    return HttpResponseBadRequest("Aucune page de référence trouvée.")
            except Exception as e:
                print(e)
                messages.error(request, f"Error sending the message: {e}")
                logger.error(f"Error sending the message: {e}")
        else:
            print(form.errors)
            return render(request, 'register/new_company.html')
    context = {
        'form': form,
    }
    return redirect(request, 'dashboard/home_new_company.html', context)


def send_mail_create_project_author(request, project):
    try:
        # Envoi de mail à l'auteur du project
        site_domain = get_current_site(request)
        from_email = (
                "Project Management <" + "amedeelougbegnon3@gmail.com" + ">"
        )
        mail_subject = "Creation of Project"
        msge = render_to_string(
            "dashboard/create_project_email.html",
            {
                "username": request.user.username,
                "project_name": project.name,
                "project_description": project.description,
                "url": reverse(
                    "view_project",
                    kwargs={
                        "id": project.pk,
                    },
                ),
                "domain": site_domain,
                "scheme": "http",
            },
        )
        send_mail(
            mail_subject,
            msge,
            from_email,
            [request.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)


def send_mail_create_project_responsible(request, project):
    try:
        # Envoi de mail à l'auteur du project
        site_domain = get_current_site(request)
        from_email = (
                "Project Management <" + "amedeelougbegnon3@gmail.com" + ">"
        )
        mail_subject = "Creation of Project"
        msge = render_to_string(
            "dashboard/create_project_email_responsible.html",
            {
                "username": project.responsible.username,
                "project_name": project.name,
                "project_description": project.description,
                "url": reverse(
                    "view_project",
                    kwargs={
                        "id": project.pk,
                    },
                ),
                "domain": site_domain,
                "scheme": "http",
            },
        )
        send_mail(
            mail_subject,
            msge,
            from_email,
            [project.responsible.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)


def send_mail_create_task_author(request, task):
    try:
        # Envoi de mail à l'auteur du project
        site_domain = get_current_site(request)
        from_email = (
                "Project Management <" + "amedeelougbegnon3@gmail.com" + ">"
        )
        mail_subject = "Creation of Task"
        msge = render_to_string(
            "dashboard/create_task_email.html",
            {
                "username": request.user.username,
                "task_name": task.name,
                "task_description": task.description,
                "url": reverse(
                    "view_task",
                    kwargs={
                        "id": task.pk,
                    },
                ),
                "domain": site_domain,
                "scheme": "http",
            },
        )
        send_mail(
            mail_subject,
            msge,
            from_email,
            [request.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)


def send_mail_create_task_responsible(request, task):
    try:
        site_domain = get_current_site(request)
        from_email = (
                "Project Management <" + "amedeelougbegnon3@gmail.com" + ">"
        )
        mail_subject = "Creation of Task"
        msge = render_to_string(
            "dashboard/create_task_email_responsible.html",
            {
                "username": task.responsible.username,
                "task_name": task.name,
                "task_description": task.description,
                "url": reverse(
                    "view_task",
                    kwargs={
                        "id": task.pk,
                    },
                ),
                "domain": site_domain,
                "scheme": "http",
            },
        )
        send_mail(
            mail_subject,
            msge,
            from_email,
            [task.responsible.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)


@login_required(login_url="/login_auth/")
def view_project(request, id):
    try:
        project = Project.objects.get(pk=id)
        chart_html = None
        tasks = Task.objects.filter(project=project)

        formMail = SendMailForm()
        company = Company.objects.get(pk=request.user.company.id)
        tasks_for_diagram = Task.objects.filter(project = id)

        if tasks_for_diagram.exists():
            task_data = [
                {"Task": task.name, "Start": task.start_date, "Finish": task.end_date}
                for task in tasks_for_diagram
            ]
            fig = px.timeline(task_data, x_start="Start", x_end="Finish", y="Task", title="Diagramme de Gantt")
            fig.update_yaxes(categoryorder="total ascending")
            chart_html = fig.to_html()

        if request.method == "POST":
            print("1")
            form = AddTaskForm(request.POST, project=project)
            print("2")
            if form.is_valid():
                print(request.POST)

                # print(form.responsible)
                print("before")
                task = form.save(commit=False)
                print("hjbhhvbfjbjfdk")
                task.project = project
                print("jh,ihjhj")
                task.author = request.user
                print("vcbvbcvng")

                # print(task.assign)
                print(task.responsible)
                if not task.responsible:
                    task.responsible = request.user
                    print(task.responsible)
                task.save()
                print('Task saved with ID:', task.id)
                print('je coince ici')
                assign_ids = request.POST.getlist('assign')  # Récupère tous les IDs d'assignés
                print("Assign IDs:", assign_ids)  # Vérifiez les IDs récupérés
                task.assign.set(assign_ids)  # Sauvegarde les relations ManyToMany (prerequisites)
                print('je dscfvdf')
                send_mail_create_task_author(request, task)
                if project.responsible:
                    send_mail_create_task_responsible(request, task)
                messages.success(
                    request,
                    f'The task "{task.name}" has been successfully created.',
                )
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
            form = AddTaskForm(project=project)
            formUpdate = UpdateProjectForm(instance=project)


        context = {
            "project": project,
            "form": form,
            "formMail": formMail,
            "tasks": tasks,
            "chart_html": chart_html,
            "segment": "projects",
            "company": company,
            "formUpdate": formUpdate,
        }
        return render(request, "dashboard/view_project.html", context)
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def update_project(request, id):
    try:
        project = Project.objects.get(pk=id)
        chart_html = None
        company = Company.objects.get(pk=request.user.company.id)

        if request.method == "POST":
            formUpdate = AddProjectForm(request.POST, instance=project)
            if formUpdate.is_valid():
                project = formUpdate.save(commit=False)
                # task.project = project
                # task.author = request.user
                # print(task.responsible)
                # if not task.responsible:
                #     task.responsible = request.user
                #     print(task.responsible)
                project.save()
                # send_mail_create_task_author(request, task)
                if project.responsible:
                    send_mail_create_project_responsible(request, project)
                messages.success(
                    request,
                    f'The Project "{project.name}" has been successfully updated.',
                )
                return redirect(
                    reverse(
                        "view_project",
                        kwargs={
                            "id": project.id,
                        },
                    )
                )
            else:
                print(formUpdate.errors)
        else:
            formUpdate = AddProjectForm(instance=project)

        context = {
            "project": project,
            "formUpdate": formUpdate,
            "chart_html": chart_html,
            "segment": "projects",
            "company": company,
        }
        return render(request, "dashboard/view_project.html", context)
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def my_tasks(request):
    try:
        print(request.user.id)
        tasks = Task.objects.filter(Q(responsible=request.user) | Q(assign=request.user))
        print(tasks)
        company = Company.objects.get(pk=request.user.company.id)

        context = {
            "tasks": tasks,
            "segment": "tasks",
            "company": company,
        }
        return render(request, "dashboard/my_tasks.html", context)
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )

@login_required(login_url="/login_auth/")
def view_task(request, id):
    try:
        task = Task.objects.get(pk=id)
        project = Project.objects.get(pk=task.project.id)
        author_company = User.objects.get(pk=project.author.id)
        employees = User.objects.filter(company=author_company.company)
        comments = task.tasks.filter(active=True)
        company = Company.objects.get(pk=request.user.company.id)
        new_comment = None
        if request.method == "POST":
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                new_comment.author = request.user
                new_comment.task = task
                new_comment.save()

                return redirect(
                    reverse(
                        "view_task",
                        kwargs={
                            "id": task.id,
                        },
                    )
                )
            else:
                print(comment_form.errors)
        else:
            comment_form = CommentForm()

        context = {
            "task": task,
            'comments': comments,
            'employees': employees,
            'new_comment': new_comment,
            'comment_form': comment_form,
            "company": company,
            "segment": "tasks",
        }
        return render(request, "dashboard/view_task.html", context)
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def update_assignation(request, id):
    try:
        task = Task.objects.get(pk=id)
        company = Company.objects.get(pk=request.user.company.id)
        new_comment = None
        if request.method == "POST":
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                new_comment.author = request.user
                new_comment.task = task
                new_comment.save()

                return redirect(
                    reverse(
                        "view_task",
                        kwargs={
                            "id": task.id,
                        },
                    )
                )
            else:
                print(comment_form.errors)
        else:
            comment_form = CommentForm()

        context = {
            "task": task,
            "company": company,
            'new_comment': new_comment,
            'comment_form': comment_form
        }
        return render(request, "dashboard/view_task.html", context)
    except Exception as e:
        print(e)
        return redirect(
            "404",
        )


@login_required(login_url="/login_auth/")
def start_task(request, id):
    try:
        task = Task.objects.get(pk=id)
        project = Project.objects.get(project=task)
        task.start()
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
    projects = Project.objects.filter(author=request.user).order_by('-creation_date')

    total_projects = projects.count()

    # Compte le nombre de projets réussis (par exemple, complétion > 100%)
    successful_projects = projects.filter(complete_percentage__gt=100).count()

    # Calcul du taux de succès
    if total_projects > 0:
        success_rate = (successful_projects / total_projects) * 100
    else:
        success_rate = 0  # Pas de projets, donc le taux de succès est 0

    # Affichage du taux de succès
    print(f"Taux de succès: {success_rate:.2f}%")

    employees_count = User.objects.filter(company=request.user.company)
    success_rate = 0
    # User.objects.exclude(role__in=[1, 5]),
    for project in projects:
        pass
        # project.author =

    company = Company.objects.get(pk=request.user.company.id)
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
        "segment": "projects",
        "projects": projects,
        "projects_count": projects.count(),
        "employees_count": employees_count.count(),
        "success_rate": success_rate,
        "formProject": formProject,
        "company": company,
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
    company = Company.objects.get(pk=request.user.company.id)
    context = {
        'segment': 'profile',
        "company": company,
    }
    return render(request, 'dashboard/profile.html', context)


@login_required(login_url="/login_auth/")
def company_profile(request, id):
    company = Company.objects.get(pk=id)
    employees = User.objects.filter(company=request.user.company)
    print(employees)
    if request.method == 'POST':
        formUpdateEmailCompany = UpdateCompanyForm(request.POST, instance=company)
        if formUpdateEmailCompany.is_valid():
            company.email = formUpdateEmailCompany.cleaned_data.get("email")
            company.social_name = formUpdateEmailCompany.cleaned_data.get("social_name")
            company.name = formUpdateEmailCompany.cleaned_data.get("name")
            company.address = formUpdateEmailCompany.cleaned_data.get("address")
            company = formUpdateEmailCompany.save()
            company.save()
            msg = "Your company information has been updated!"
            messages.success(request, msg)
            return redirect(
                reverse(
                    "company_profile",
                    kwargs={
                        "id": id,
                    },
                )
            )
        else:
            print(formUpdateEmailCompany.errors)
    else:
        formInvite = InviteForm()
        formUpdateEmailCompany = UpdateCompanyForm(instance=company)
    context = {
        'segment': 'companyprofile',
        'company': company,
        "employees": employees,
        'formUpdateEmailCompany': formUpdateEmailCompany,
        "formInvite": formInvite,
    }
    return render(request, 'dashboard/company_profile.html', context)


# @login_required(login_url="/login_auth/")
# def update_company(request):
#     context = {
#
#     }
#     referer = request.META.get('HTTP_REFERER')
#     if referer:
#         return redirect(referer)
#     else:
#         return redirect("home")


@login_required(login_url="/login_auth/")
def invite_company(request, id):
    company_id = id
    company = Company.objects.get(pk=id)
    site_domain = get_current_site(request)
    mail_subject = f"The company {company.name} invited you to join its team"
    from_email = settings.DEFAULT_FROM_EMAIL
    formInvite = InviteForm(request.POST)
    if formInvite.is_valid():
        # for form in formset:
        print("ici")
        message = request.POST.get("message")
        email = request.POST.get("email")
        # user_exist =
        if User.objects.filter(email=email).exists():
            print('User already exist')
            msg = "Specified email address already exist. Please contact the Project management Support."
            messages.error(request, msg)
            logger.error(f"Error : {msg}")
        else:
            if email != "":
                message = render_to_string(
                    "dashboard/email_template_invite.html",
                    {
                        "company": company.name,
                        "message": message,
                        "url": reverse(
                            "acceptation_invitation_new_user",
                            kwargs={"company_id": company.id},
                        ),
                        "domain": site_domain,
                        "scheme": "http",
                    },
                )
                try:
                    send_mail(
                        mail_subject,
                        message,
                        from_email,
                        [email],
                        fail_silently=False,
                    )
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "Project management sent you an email to {0}.".format(email),
                    )
                    logger.info(
                        f"Send invitation email for {email}"
                    )
                except Exception as e:
                    msg = "Project management was unable to send a verification message to the specified email address. Please contact the Project management Support."
                    messages.error(request, msg)
                    logger.error(f"Error sending the verification message: {e}")
                return redirect(
                    reverse(
                        "company_profile",
                        kwargs={
                            "id": company_id,
                        },
                    )
                )
            else:
                pass

    context = {

    }
    return redirect(
        reverse(
            "company_profile",
            kwargs={
                "id": company_id,
            },
        )
    )


def acceptation_invitation_new_user(request, company_id):
    request.session["type_account"] = "member"
    request.session["my_car"] = "mini"
    request.session["company"] = company_id
    return redirect("register")