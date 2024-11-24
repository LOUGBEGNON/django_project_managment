from django.core.exceptions import ValidationError
from django.db import models
from apps.authentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

STATUS_CHOICE = (
    (0, 'CREATED'),
    (1, 'IN PROGRESS'),
    (2, "PAUSED"),
    (3, "COMPLETED")
)

DUE_CHOICE = (
    (1, 'On Due'),
    (2, 'Overdue'),
    (3, 'Done'),
)

class Project(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(blank=True)
    slug = models.SlugField('slugproject', blank=True)
    # assign = models.ManyToManyField(User)
    # efforts = models.DurationField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE, default=0, blank=True, null=True)
    dead_line = models.DateTimeField()
    author = models.ForeignKey(
        'authentication.User', related_name="project_author", on_delete=models.DO_NOTHING
    )
    complete_percentage = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)], default=0)
    responsible = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return (self.name)

    @property
    def completion_percentage(self):
        tasks = self.project.all()  # Récupère toutes les tâches associées
        if not tasks:
            return 0  # Si aucune tâche, le pourcentage est 0

        completed_tasks = sum(1 for task in tasks if task.is_completed)
        percentage = (completed_tasks / len(tasks)) * 100
        self.complete_percentage = round(percentage)  # Arrondit à l'entier le plus proche
        self.save()
        return round(percentage)

    @property
    def get_status(self):
        if self.status == 0:
            project_status = 'CREATED'
        if self.status == 1:
            project_status = 'IN PROGRESS'
        if self.status == 2:
            project_status = "PAUSED"
        if self.status == 3:
            project_status = "COMPLETED"
        return project_status


class Task(models.Model):
    completion_date = models.DateTimeField(null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project"
    )
    assign = models.ManyToManyField(User, related_name="assign_tasks")
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE, default=0, blank=True, null=True)
    due = models.PositiveSmallIntegerField(choices=DUE_CHOICE, default=1, blank=True, null=True)
    current_start_time = models.DateTimeField(null=True)
    responsible = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(
        User, related_name="task_author", on_delete=models.DO_NOTHING
    )
    total_duration = models.DurationField(
        null=True,
        default=timedelta(seconds=0)
    )
    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="subsequent_tasks"
    )
    creation_date = models.DateTimeField(
        _("creation date"),
        blank=True,
        db_index=True,
        default=timezone.now,
        help_text=_("Creation date, by default it is now."),)
    update_date = models.DateField(_
        ("update date"),
        blank=True,
        db_index=True,
        default=timezone.now,
        help_text=_("Update date, by default it is now."),)
    start_date = models.DateField(
        ("start date"),
        blank=True,
        db_index=True,
        default=timezone.now,
        help_text=_("Start date, by default it is now."),)
    end_date = models.DateField(
        _("end date"),
        blank=True,
        db_index=True,
        default=timezone.now,
        help_text=_("End date, by default it is now."),
    )

    class Meta:
        db_table = "task"
        ordering = ['project', 'name']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return "{}, {}".format(self.name, self.status)

    @property
    def is_created(self):
        return self.status == 0

    @property
    def is_in_progress(self):
        return self.status == 1

    @property
    def is_paused(self):
        return self.status == 2

    @property
    def is_completed(self):
        return self.status == 3

    @property
    def incomplete_prerequisites(self):
        """
        Renvoie la liste des prérequis qui ne sont pas encore complétés.
        """
        return self.prerequisites.exclude(status=3)

    def start(self):
        """
            Démarre la tâche si tous les prérequis sont complétés.
            """
        if not self.allowed_to_start:
            raise ValueError("Impossible de démarrer la tâche. Tous les prérequis ne sont pas encore complétés.")
        self.current_start_time = timezone.now()
        self.status = 1
        self.save()

    def complete(self):
        self.completion_date = timezone.now()
        self.total_duration += timezone.now() - self.completion_date
        self.status = 3
        self.save()

    def pause(self):
        difference = timezone.now() - self.current_start_time
        self.total_duration += difference
        self.status = 2
        self.save()

    @property
    def allowed_to_start(self):
        """
        Vérifie si tous les prérequis de cette tâche sont complétés.
        """
        return all(prerequisite.status == 3 for prerequisite in self.prerequisites.all())

    @property
    def get_status(self):
        project_status = ""
        if self.status == 0:
            project_status = 'CREATED'
        if self.status == 1:
            project_status = 'IN PROGRESS'
        if self.status == 2:
            project_status = "PAUSED"
        if self.status == 3:
            project_status = "COMPLETED"
        return project_status


    # def clean(self):
    #     """
    #     Valide qu'il n'y a pas de cycles dans les prérequis.
    #     """
    #
    #     def has_cycle(task, visited):
    #         if task in visited:
    #             return True
    #         visited.add(task)
    #         for prerequisite in task.prerequisites.all():
    #             if has_cycle(prerequisite, visited):
    #                 return True
    #         visited.remove(task)
    #         return False
    #
    #     if has_cycle(self, set()):
    #         raise ValidationError("Impossible d'ajouter ce prérequis : cela crée un cycle.")


class Comment(models.Model):
    author = models.ForeignKey(
        User, related_name="comment_author", on_delete=models.DO_NOTHING
    )
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='tasks')
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.message, self.message)


class Company(models.Model):
    responsible = models.ForeignKey(
        User, related_name="company_responsible", on_delete=models.DO_NOTHING, default=1
    )
    social_name = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    found_date = models.DateField(default=timezone.now,)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = 'Companies'
        ordering = ('name',)

    def __str__(self):
        return (self.name)


# Model for employees, linked to users
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    position = models.CharField(max_length=100)

    class Meta:
        db_table = "employee"

    def __str__(self):
        return self.name


# Model for teams
class Team(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="teams"
    )
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "team"
        verbose_name = "Team"
        verbose_name_plural = "Teams"


# Model for notifications
class Notification(models.Model):
    description = models.CharField(max_length=100)
    notification_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    class Meta:
        db_table = "notification"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


# Model for Gantt chart
class GanttChart(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='gantt_entries')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = "gantt_chart"
        verbose_name = "GanttChart"
        verbose_name_plural = "GanttCharts"

