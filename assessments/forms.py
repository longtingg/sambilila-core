from django import forms
from django.forms import modelformset_factory
from .models import StudentGrade

class StudentGradeForm(forms.ModelForm):
    class Meta:
        model = StudentGrade
        fields = ['student', 'raw_score', 'teacher_remarks']
        widgets = {
            # Hide the student ID but keep it in the form data submit loop
            'student': forms.HiddenInput(),
            'raw_score': forms.NumberInput(attrs={
                'class': 'form-control score-field', 
                'min': '0', 
                'step': '0.5',
                'placeholder': 'Score'
            }),
            'teacher_remarks': forms.TextInput(attrs={
                'class': 'form-control remarks-field', 
                'placeholder': 'Add performance remarks (optional)'
            }),
        }

# Base FormSet configuration to easily control bulk records
BaseStudentGradeFormSet = modelformset_factory(
    StudentGrade,
    form=StudentGradeForm,
    extra=0,  # No extra empty forms; we only generate forms for existing students
)
