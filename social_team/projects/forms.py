from django import forms

from .models import Project, Position


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'time_line', 'requirementes']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'circle--input--h1',
                       'placeholder': 'Project Title'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Project description...'}),
            'time_line': forms.Textarea(
                attrs={'class': 'circle--textarea--input',
                       'placeholder': 'Time estimate'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'description']


PositionFormSet = forms.modelformset_factory(
    Position,
    form=PositionForm,
    extra=1,
)

PositionInlineFormSet = forms.inlineformset_factory(
    Project,
    Position,
    extra=0,
    fields=('name', 'description', 'skill'),
    formset=PositionFormSet,
    min_num=1,
    widgets={
        'name': forms.TextInput(
            attrs={'class': 'circle--input--h3',
                   'placeholder': 'Position Title'}),
        'description': forms.Textarea(
            attrs={'placeholder': 'Position description...'}),
    },
    labels={
        'name': '',
        'description': ''
    }
)
