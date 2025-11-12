from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory  # ← ADD THIS LINE
from . import models

# Import models individually to avoid circular import issues
DispensedDrug = models.DispensedDrug
LabResult = models.LabResult
Drug = models.Drug
LabTest = models.LabTest
PatientEMR = models.PatientEMR
LabRequest = models.LabRequest  # ← NOW SAFE
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

# -------------------------------------------------
# Nurse forms
# -------------------------------------------------
class NurseUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}

class NurseForm(forms.ModelForm):
    class Meta:
        model = models.Nurse
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']

class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = models.VitalSigns
        fields = ['temperature', 'blood_pressure', 'pulse_rate', 'respiratory_rate', 
                 'oxygen_saturation', 'weight', 'height', 'notes']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 120/80'}),
            'pulse_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'oxygen_saturation': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# -------------------------------------------------
# Account Department Forms
# -------------------------------------------------
class AccountUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {'password': forms.PasswordInput()}

class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ['address', 'mobile', 'profile_pic']

# -------------------------------------------------
# Billing forms
# -------------------------------------------------
class BillForm(forms.ModelForm):
    class Meta:
        model = models.Bill
        fields = ['status', 'discount', 'payment_method', 'insurance_details', 'remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'insurance_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BillItemForm(forms.ModelForm):
    class Meta:
        model = models.BillItem
        fields = ['item_type', 'description', 'quantity', 'unit_price']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

BillItemFormSet = inlineformset_factory(
    models.Bill,
    models.BillItem,
    form=BillItemForm,
    fields=('item_type', 'description', 'quantity', 'unit_price'),
    extra=3,
    can_delete=True
)

class DischargeForm(forms.Form):
    room_charge = forms.DecimalField(
        label='Room Charges per Day',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    doctor_fee = forms.DecimalField(
        label='Doctor Fee',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    discharge_summary = forms.CharField(
        label='Discharge Summary',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
    other_charges = forms.DecimalField(
        label='Other Charges',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
        initial=0
    )

# ──────────────────────────────────────────────────────────────
#  Doctor: Add lab request inside EMR
# ──────────────────────────────────────────────────────────────
class LabRequestForm(forms.ModelForm):
    class Meta:
        model = LabRequest
        fields = ['test_name']
        widgets = {
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CBC, LFT, Urine R/E'
            })
        }

# Inline formset so doctor can add many tests at once
LabRequestFormSet = inlineformset_factory(
    PatientEMR, LabRequest,
    form=LabRequestForm,
    extra=2,
    can_delete=True
)

# ──────────────────────────────────────────────────────────────
#  Lab Tech: Fill result for a request
# ──────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────
#  Lab Tech: Fill result – can see ordered test + edit if needed
# ──────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────
#  Lab Tech: Fill result – can see ordered test + edit if needed
# ──────────────────────────────────────────────────────────────
class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['test_name', 'result_value', 'remarks']
        widgets = {
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Full Blood Count (FBC)'
            }),
            'result_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 12.5 g/dL, Positive, Normal'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any observations or flags'
            }),
        }

    def __init__(self, *args, lab_request=None, **kwargs):
        super().__init__(*args, **kwargs)
        if lab_request:
            self.fields['test_name'].initial = lab_request.test_name
            self.fields['test_name'].widget.attrs['readonly'] = False
            self.fields['test_name'].help_text = (
                f"<small class='text-muted'>"
                f"Ordered: <strong>{lab_request.test_name}</strong> "
                f"by Dr. {lab_request.ordered_by.get_full_name() if lab_request.ordered_by else 'Unknown'} "
                f"on {lab_request.ordered_at.strftime('%d %b %Y, %I:%M %p')}"
                f"</small>"
            )
        else:
            self.fields['test_name'].help_text = ""
# --- EMR Form (for doctor) ---
# hospital/forms.py

class PatientEMRForm(forms.ModelForm):
    class Meta:
        model = models.PatientEMR
        fields = ['diagnosis', 'symptoms', 'treatment', 'prescription', 'notes']
        widgets = {
            'diagnosis': forms.TextInput(attrs={'class': 'form-control'}),
            'symptoms': forms.TextInput(attrs={'class': 'form-control'}),
            'treatment': forms.TextInput(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
