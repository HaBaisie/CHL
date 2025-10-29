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
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Receipt #{self.pk} – {self.patient.get_name}"


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