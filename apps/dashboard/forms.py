
from django import forms
from .models import (
    Project,
)
from apps.authentication.models import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


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

    slug = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Project Slug",
                "class": "form-control text-center",
            }
        ),
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
            "slug",  # only on Update forms
            "responsible",
        ]

