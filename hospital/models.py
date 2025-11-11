from django.db import models
from django.contrib.auth.models import User



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"

class PatientEMR(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emr_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField(max_length=500, blank=True, null=True)
    symptoms = models.TextField(max_length=500, blank=True, null=True)
    treatment = models.TextField(max_length=500, blank=True, null=True)
    prescription = models.TextField(max_length=500, blank=True, null=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    tests = models.TextField(max_length=500, blank=True, null=True)
    is_discharged = models.BooleanField(default=False)

    def __str__(self):
        return f"EMR - {self.patient.get_name} | Dr. {self.doctor.get_name}"

class Appointment(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)
    emr = models.ForeignKey(PatientEMR, on_delete=models.SET_NULL, null=True, blank=True)  # Link to EMR


class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

# -------------------------------------------------
# 1. DRUG CATALOGUE (Pharmacy)
# -------------------------------------------------
class Drug(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=30)          # e.g. Tablet, ml, vial
    default_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} ({self.unit})"

# -------------------------------------------------
# 2. DISPENSED DRUGS (linked to a prescription)
# -------------------------------------------------
class DispensedDrug(models.Model):
    emr = models.ForeignKey(PatientEMR, on_delete=models.CASCADE, related_name='dispensed_drugs')
    drug_name = models.CharField(max_length=200)  # NEW: Free text
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    dispensed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dispensed_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"{self.drug_name} x {self.quantity}"
    
# -------------------------------------------------
# 3. PHARMACY RECEIPT (one per dispense session)
# -------------------------------------------------
class PharmacyReceipt(models.Model):
    dispensed_drugs = models.ManyToManyField(DispensedDrug)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('final', 'Final'),
        ('cancelled', 'Cancelled')
    ], default='draft')

    def __str__(self):
        return f"Receipt #{self.pk} – {self.patient.get_name} ({self.status})"

    def recalculate_total(self):
        total = sum(drug.total() for drug in self.dispensed_drugs.all())
        self.total_amount = total
        self.save()


# -------------------------------------------------
# 4. LAB TEST CATALOGUE
# -------------------------------------------------
class LabTest(models.Model):
    code = models.CharField(max_length=20, unique=True)      # e.g. CBC, LFT
    name = models.CharField(max_length=150)
    normal_range = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.code} – {self.name}"

# -------------------------------------------------
# 5. LAB RESULT (one per test per patient)
# -------------------------------------------------
class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=150)  # NEW: Free text
    result_value = models.CharField(max_length=200)
    remarks = models.TextField(blank=True)
    performed_at = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.test_name} – {self.patient.get_name}"
    

# -------------------------------------------------
# PHARMACY PROFILE MODEL
# -------------------------------------------------
class Pharmacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/PharmacyProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return f"Pharmacy: {self.get_name}"


# -------------------------------------------------
# LAB TECHNICIAN PROFILE MODEL
# -------------------------------------------------
class Lab(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/LabProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return f"Lab Technician: {self.get_name}"

# -------------------------------------------------
# NURSE PROFILE MODEL
# -------------------------------------------------
class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/NurseProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return f"Nurse: {self.get_name}"

# -------------------------------------------------
# VITAL SIGNS MODEL
# -------------------------------------------------
class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_pressure = models.CharField(max_length=20)
    pulse_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    oxygen_saturation = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.patient.get_name} taken by {self.nurse.get_name}"

# -------------------------------------------------
# ACCOUNT DEPARTMENT MODELS
# -------------------------------------------------
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/AccountProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return f"Accountant: {self.get_name}"

# -------------------------------------------------
# BILLING MODELS
# -------------------------------------------------
class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    generated_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discharge_summary = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('insurance', 'Insurance'),
        ('transfer', 'Bank Transfer')
    ], default='cash')
    insurance_details = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    def calculate_total(self):
        # Calculate total from all bill items
        total = self.billitem_set.aggregate(
            total=models.Sum('total_price'))['total'] or 0
        self.total_amount = total
        self.final_amount = total - self.discount
        self.save()
    
    def save(self, *args, **kwargs):
        self.final_amount = self.total_amount - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill #{self.pk} for {self.patient.get_name}"

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20, choices=[
        ('drug', 'Pharmacy Drug'),
        ('lab', 'Laboratory Test'),
        ('service', 'Medical Service'),
        ('room', 'Room Charges'),
        ('doctor', 'Doctor Fee'),
        ('other', 'Other Charges')
    ])
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=50, blank=True, null=True)  # For linking to source records
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Update bill total
        self.bill.calculate_total()

    def __str__(self):
        return f"{self.item_type}: {self.description}"
    
# ──────────────────────────────────────────────────────────────
#  LAB REQUEST (Doctor orders a test)
# ──────────────────────────────────────────────────────────────
class LabRequest(models.Model):
    emr = models.ForeignKey(PatientEMR, on_delete=models.CASCADE, related_name='lab_requests')
    test_name = models.CharField(max_length=200)      # e.g. "Full Blood Count"
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ordered_tests')
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_name} for {self.emr.patient.get_name}"