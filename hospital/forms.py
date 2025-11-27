# hospital/forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from cloudinary.forms import CloudinaryFileField  # ← THIS IS THE KEY LINE

from . import models

# Import models to avoid circular imports
DispensedDrug = models.DispensedDrug
LabResult = models.LabResult
PatientEMR = models.PatientEMR
LabRequest = models.LabRequest


# ------------------------------------------------------------------
# ADMIN SIGNUP
# ------------------------------------------------------------------
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}


# ------------------------------------------------------------------
# DOCTOR FORMS
# ------------------------------------------------------------------
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}

class DoctorForm(forms.ModelForm):
    profile_pic = CloudinaryFileField(
        required=False,
        options={'folder': 'profile_pic/DoctorProfilePic', 'crop': 'thumb', 'width': 200, 'height': 200}
    )

    class Meta:
        model = models.Doctor
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']


# ------------------------------------------------------------------
# PATIENT FORMS
# ------------------------------------------------------------------
class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}

# hospital/forms.py

# hospital/forms.py

# hospital/forms.py

class PatientForm(forms.ModelForm):
    profile_pic = CloudinaryFileField(
        required=False,
        options={'folder': 'profile_pic/PatientProfilePic', 'crop': 'thumb', 'width': 200, 'height': 200}
    )

    class Meta:
        model = models.Patient
        fields = ['address', 'mobile', 'symptoms', 'assignedDoctorId', 'profile_pic']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 08123456789'}),
            'symptoms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Fever, Headache'}),
            # DO NOT override assignedDoctorId here → we handle it in template
        }
# ------------------------------------------------------------------
# APPOINTMENT FORMS
# ------------------------------------------------------------------
class AppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(
        queryset=models.Doctor.objects.filter(status=True),
        empty_label="Select Doctor", to_field_name="user_id"
    )
    patientId = forms.ModelChoiceField(
        queryset=models.Patient.objects.filter(status=True),
        empty_label="Select Patient", to_field_name="user_id"
    )

    class Meta:
        model = models.Appointment
        fields = ['description', 'status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(
        queryset=models.Doctor.objects.filter(status=True),
        empty_label="Select Doctor", to_field_name="user_id"
    )

    class Meta:
        model = models.Appointment
        fields = ['description', 'status']


# ------------------------------------------------------------------
# CONTACT FORM
# ------------------------------------------------------------------
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))


# ------------------------------------------------------------------
# PHARMACY FORMS
# ------------------------------------------------------------------
class DispenseDrugForm(forms.ModelForm):
    class Meta:
        model = DispensedDrug
        fields = ['drug_name', 'quantity', 'price_per_unit']
        widgets = {
            'drug_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Amoxicillin 500mg'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
        }

DispenseDrugFormSet = inlineformset_factory(
    models.PatientEMR, DispensedDrug,
    form=DispenseDrugForm,
    fields=('drug_name', 'quantity', 'price_per_unit'),
    extra=3, can_delete=True
)


# ------------------------------------------------------------------
# PHARMACY, LAB, NURSE, ACCOUNT SIGNUP FORMS
# ------------------------------------------------------------------
class PharmacyUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}

class PharmacyForm(forms.ModelForm):
    profile_pic = CloudinaryFileField(required=False, options={'folder': 'profile_pic/PharmacyProfilePic'})
    class Meta:
        model = models.Pharmacy
        fields = ['address', 'mobile', 'profile_pic']


class LabUserForm(PharmacyUserForm): pass
class LabForm(forms.ModelForm):
    profile_pic = CloudinaryFileField(required=False, options={'folder': 'profile_pic/LabProfilePic'})
    class Meta:
        model =models.Lab
        fields = ['address', 'mobile', 'profile_pic']


class NurseUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}

class NurseForm(forms.ModelForm):
    profile_pic = CloudinaryFileField(required=False, options={'folder': 'profile_pic/NurseProfilePic'})
    class Meta:
        model = models.Nurse
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']


class AccountUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}

class AccountForm(forms.ModelForm):
    profile_pic = CloudinaryFileField(required=False, options={'folder': 'profile_pic/AccountProfilePic'})
    class Meta:
        model = models.Account
        fields = ['address', 'mobile', 'profile_pic']


# ------------------------------------------------------------------
# BILLING & DISCHARGE
# ------------------------------------------------------------------
class BillForm(forms.ModelForm):
    class Meta:
        model = models.Bill
        fields = ['status', 'discount', 'payment_method', 'insurance_details', 'remarks']

class BillItemForm(forms.ModelForm):
    class Meta:
        model = models.BillItem
        fields = ['item_type', 'description', 'quantity', 'unit_price']

BillItemFormSet = inlineformset_factory(
    models.Bill, models.BillItem,
    form=BillItemForm,
    fields=('item_type', 'description', 'quantity', 'unit_price'),
    extra=3, can_delete=True
)

class DischargeForm(forms.Form):
    room_charge = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    doctor_fee = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    other_charges = forms.DecimalField(min_value=0, decimal_places=2, required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    discharge_summary = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))


# ------------------------------------------------------------------
# LAB REQUEST & EMR FORMS
# ------------------------------------------------------------------
class LabRequestForm(forms.ModelForm):
    class Meta:
        model = LabRequest
        fields = ['test_name']
        widgets = {'test_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Full Blood Count'})}

LabRequestFormSet = inlineformset_factory(PatientEMR, LabRequest, form=LabRequestForm, extra=2, can_delete=True)

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['test_name', 'result_value', 'remarks']
        widgets = {
            'test_name': forms.TextInput(attrs={'class': 'form-control'}),
            'result_value': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, lab_request=None, **kwargs):
        super().__init__(*args, **kwargs)
        if lab_request:
            self.fields['test_name'].initial = lab_request.test_name
            self.fields['test_name'].widget.attrs['readonly'] = True


class PatientEMRForm(forms.ModelForm):
    class Meta:
        model = models.PatientEMR
        fields = ['diagnosis', 'symptoms', 'treatment', 'prescription', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'treatment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }