from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    """
    Form for adding and updating employees.Includes validation for email and phone fields.
    """
    class Meta:
        #The Meta class is used to define metadata for the form
        model = Employee
        fields = ['name', 'department', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter department name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        }
        labels = {
            'name': 'Employee Name',
            'department': 'Department',
            'email': 'Email Address',
            'phone': 'Phone Number',
        }

    def clean_email(self):
        """
        Validates the email field to ensure a proper valid email format.
        self refers to the specific instance of the class on which the method is being called.
        self is similar to 'this' keyword
        """
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email field cannot be empty.")
        if not "@" in email:
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_phone(self):
        """
        Validates the phone field to ensure it contains only digits and has 10 digit length.
        """
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
          raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
          raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone
