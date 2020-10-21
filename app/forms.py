from .models import Student, Marks
from django.forms import ModelForm


class StudentCreationForm(ModelForm):
    class Meta:
        model = Student
        fields = ('student_roll', 'student_class','student_name')


class MarksCreationForm(ModelForm):
    class Meta:
        model = Marks
        fields = "__all__"
