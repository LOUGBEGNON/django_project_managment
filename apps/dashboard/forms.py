
from django import forms
from .models import (
    Project, Task, Comment, Company
)
from apps.authentication.models import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput
from django.forms import modelformset_factory

# class XDSoftDateTimePickerInput(forms.DateTimeInput):
#     template_name = "dashboard/xdsoft_datetimepicker.html"


class AddProjectForm(forms.ModelForm):
    """ """

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Project name",
                "autocomplete": "name",
            },
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Project description",
                "autocomplete": "description",
            },
        )
    )


    dead_line = forms.DateTimeField(
        input_formats=["%d/%m/%Y"],
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "dd/mm/yyyy",
                "name": "dead_line",
            }
        ),
    )

    responsible = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.exclude(role__in=[1, 5]),
        empty_label="Project Responsible",
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "dead_line",
            # "slug",  # only on Update forms
            "responsible",
        ]


class UpdateProjectForm(forms.ModelForm):
    """ """

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Project name",
                "autocomplete": "name",
            },
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Project description",
                "autocomplete": "description",
            },
        )
    )


    dead_line = forms.DateTimeField(
        input_formats=["%d/%m/%Y"],
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "dd/mm/yyyy",
                "name": "dead_line",
            }
        ),
    )

    responsible = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.exclude(role__in=[1, 5]),
        empty_label="Project Responsible",
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "dead_line",
            "responsible",
        ]


class AddCompanyForm(forms.ModelForm):
    """ """
    social_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company Social name",
                "autocomplete": "name",
            },
        )
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company name",
                "autocomplete": "name",
            },
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Company address",
                "autocomplete": "address",
            },
        )
    )

    class Meta:
        model = Company
        fields = [
            "social_name",
            "name",
            "email",
            "address",
        ]


class AddTaskForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Task name",
                "autocomplete": "name",
            },
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Task description",
                "autocomplete": "description",
            },
        )
    )

    responsible = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.exclude(role__in=[1, 5]),
        empty_label="Task Responsible",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    assign = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.exclude(role__in=[1, 5]),
        empty_label="Task assign",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    start_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y"],
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "dd/mm/yyyy",
                "name": "start_date",
            }
        ),
    )

    end_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y"],
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "dd/mm/yyyy",
                "name": "end_date",
            }
        ),
    )

    prerequisites = forms.ModelMultipleChoiceField(
        queryset=Task.objects.none(),  # Par défaut, aucune tâche n'est affichée
        required=False,
        widget=forms.CheckboxSelectMultiple,  # Liste de cases à cocher
        label="Prérequis",
    )

    def clean_prerequisites(self):
        """
        Vérifie que la tâche n'a pas de cycle dans les prérequis.
        """
        prerequisites = self.cleaned_data.get('prerequisites', [])
        if self.instance.pk and self.instance in prerequisites:
            raise forms.ValidationError("Une tâche ne peut pas être un prérequis d'elle-même.")
        return prerequisites

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Récupère le projet passé au formulaire
        super().__init__(*args, **kwargs)
        if project:
            # Filtre les tâches liées uniquement au projet donné
            self.fields['prerequisites'].queryset = Task.objects.filter(project=project)

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            # "assign",
            "responsible",
            'prerequisites',
        ]


class UpdateTaskForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Task name",
                "autocomplete": "name",
            },
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Task description",
                "autocomplete": "description",
            },
        )
    )

    responsible = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.exclude(role__in=[1, 5]),
        empty_label="Task Responsible",
    )

    assign = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.exclude(role__in=[1, 5]),
        empty_label="Task assign",
    )

    start_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y"],
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "dd/mm/yyyy",
                "name": "start_date",
            }
        ),
    )

    end_date = forms.DateTimeField(
        input_formats=["%d/%m/%Y"],
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "placeholder": "dd/mm/yyyy",
                "name": "end_date",
            }
        ),
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "assign",
            "responsible",
        ]


class CommentForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Task comment",
                "autocomplete": "message",
            },
        )
    )

    class Meta:
        model = Comment
        fields = ('message',)


class SendMailForm(forms.Form):
    """ """
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subject Mail",
                "autocomplete": "subject",
            },
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Content",
                "autocomplete": "message",
            },
        )
    )


class InviteForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Content",
                "autocomplete": "message",
            },
        )
    )


InvitationFormSet = modelformset_factory(
    User,
    fields=("email",),
    extra=1,
    widgets={
        # "message": forms.CharField(
        #     widget=forms.Textarea(
        #         attrs={
        #             "class": "form-control",
        #             "placeholder": "Content",
        #             "autocomplete": "message",
        #         },
        #     )
        # ),

        "email": forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "type": "email",
            }
        )
    },
)