from django import forms
from .models import Employee


class MyForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields='__all__'

# class MyForm(forms.Form):
#     emp_id=forms.IntegerField()
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField()
#     email=forms.EmailField()
#     mobileno=forms.IntegerField()
#     gender=forms.CharField()
#     created_at= forms.DateField()
#     updated_at=forms.DateField()





