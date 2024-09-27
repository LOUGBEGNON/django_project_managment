from django.db import models
from apps.authentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import timedelta

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
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, default=STATUS_CHOICE[0])
    dead_line = models.DateField()
    author = models.ForeignKey(
        User, related_name="project_author", on_delete=models.DO_NOTHING
    )
    complete_percentage = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)], default=0)
    responsible = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return (self.name)


class Task(models.Model):
    completion_date = models.DateTimeField(null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    # assign = models.ManyToManyField(User)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, default=0)
    due = models.CharField(max_length=7, choices=DUE_CHOICE, default=1)
    current_start_time = models.DateTimeField(null=True)
    responsible = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
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

    class Meta:
        db_table = "task"
        ordering = ['project', 'name']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return "{}, {}".format(self.name, self.status)

    @property
    def is_created(self):
        return self.status == '0'

    @property
    def is_in_progress(self):
        return self.status == '1'

    @property
    def is_paused(self):
        return self.status == '2'

    @property
    def is_completed(self):
        return self.status == '3'

    def start(self):
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
        for prerequisite in self.prerequisites:
            if prerequisite.status != 3:
                return False
        return True


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

