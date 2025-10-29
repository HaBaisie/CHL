from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory  # ← ADD THIS LINE
from . import models
from .models import DispensedDrug, LabResult, Drug, LabTest
from .models import DispensedDrug, LabResult, Drug, LabTest, PatientEMR
#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']



#for teacher related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic']



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

# -------------------------------------------------
# Pharmacy forms
# -------------------------------------------------
# -------------------------------------------------
# Pharmacy forms
# -------------------------------------------------
class DispenseDrugForm(forms.ModelForm):
    class Meta:
        model = DispensedDrug
        fields = ['drug_name', 'quantity', 'price_per_unit']
        widgets = {
            'drug_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Paracetamol 500mg'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Qty'
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Price'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        qty = cleaned_data.get('quantity')
        price = cleaned_data.get('price_per_unit')
        if qty and price:
            cleaned_data['total'] = qty * price
        return cleaned_data


# CORRECTED: Add `fields` and `extra`
DispenseDrugFormSet = inlineformset_factory(
    models.PatientEMR,           # Parent model
    DispensedDrug,               # Child model
    form=DispenseDrugForm,
    fields=('drug_name', 'quantity', 'price_per_unit'),  # REQUIRED
    extra=3,                     # Show 3 blank rows
    can_delete=True
)

# -------------------------------------------------
# Lab forms
# -------------------------------------------------
class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['test_name', 'result_value', 'remarks']
        widgets = {
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Full Blood Count (FBC)'
            }),
            'result_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 12.5 g/dL'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                '`placeholder': 'Optional notes'
            }),
        }

class PharmacyUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {'password': forms.PasswordInput()}

class PharmacyForm(forms.ModelForm):
    class Meta:
        model = models.Pharmacy   # you will create this model (optional profile)
        fields = ['address','mobile','profile_pic']

# same for Lab
class LabUserForm(PharmacyUserForm): pass
class LabForm(PharmacyForm): pass