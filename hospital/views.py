from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from datetime import datetime, timedelta, date
# App imports
from . import models
from . import forms
from .models import (
    PatientEMR, DispensedDrug, Drug, 
    PharmacyReceipt, LabResult, Patient,LabRequest
)
 

from django.forms import inlineformset_factory

DispenseDrugFormSet = inlineformset_factory(
    PatientEMR,
    DispensedDrug,
    form=forms.DispenseDrugForm,
    fields=('drug_name', 'quantity', 'price_per_unit'),  # ← CORRECT
    extra=3,
    can_delete=True
)
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import PatientEMR, DispensedDrug, PharmacyReceipt
from .forms import DispenseDrugFormSet
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')




def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            
            patient = patientForm.save(commit=False)
            patient.user =  user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.status = True
            patient.admitDate = date.today()
            patient.save()
            
            my_patient_group, _ = Group.objects.get_or_create(name='PATIENT')
            my_patient_group.user_set.add(user)
            
            messages.success(request, "Registration successful! You can now log in.")
            return HttpResponseRedirect('patientlogin')
    
    return render(request, 'hospital/patientsignup.html', context=mydict)

#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def afterlogin_view(request):
    if request.user.groups.filter(name='ADMIN').exists():
        return redirect('admin-dashboard')
    elif request.user.groups.filter(name='DOCTOR').exists():
        return redirect('doctor-dashboard')
    elif request.user.groups.filter(name='PATIENT').exists():
        return redirect('patient-dashboard')
    elif request.user.groups.filter(name='PHARMACY').exists():
        return redirect('pharmacy-dashboard')
    elif request.user.groups.filter(name='LAB').exists():
        return redirect('lab-dashboard')
    elif request.user.groups.filter(name='NURSE').exists():
        return redirect('nurse-dashboard')
    elif request.user.groups.filter(name='ACCOUNT').exists():
        return redirect('account-dashboard')
    else:
        # Fallback: logout and show error
        from django.contrib import messages
        messages.error(request, "Invalid user role. Contact admin.")
        return redirect('logout')







#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


# In hospital/views.py

from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
import io

def render_to_pdf(template_src, context_dict={}):
    html_string = render_to_string(template_src, context_dict)
    html = HTML(string=html_string, base_url=None)
    
    # Use BytesIO to avoid file system
    result = io.BytesIO()
    
    # CRITICAL: Force UTF-8 encoding
    html.write_pdf(
        target=result,
        presentational_hints=True,
        font_config=None,
        # Add this to ensure UTF-8
        encoding='utf-8'
    )
    
    result.seek(0)
    pdf = result.getvalue()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="receipt.pdf"'
    return response



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_emr(request, patient_id):
    patient = models.Patient.objects.get(id=patient_id)
    emr_records = models.PatientEMR.objects.filter(patient=patient).order_by('-date')
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    
    # Get the latest vitals for quick reference
    latest_vitals = models.VitalSigns.objects.filter(patient=patient).order_by('-timestamp').first()
    
    context = {
        'patient': patient,
        'emr_records': emr_records,
        'doctor': doctor,  # for profile picture in sidebar
        'vitals': latest_vitals,  # Latest vitals
    }
    return render(request, 'hospital/doctor_view_patient_emr.html', context)




#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            if doctor.department == 'Cardiologist':
                if 'heart' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})


            if doctor.department == 'Dermatologists':
                if 'skin' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Allergists/Immunologists':
                if 'allergy' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Colon and Rectal Surgeons':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})





            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

# -------------------------------------------------------------------------
# PHARMACY VIEWS
# -------------------------------------------------------------------------
@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_dashboard(request):
    # show pending prescriptions (EMR with prescription field filled)
    pending = PatientEMR.objects.filter(prescription__isnull=False).exclude(
        dispensed_drugs__isnull=False).distinct()
    context = {'pending': pending}
    return render(request, 'hospital/pharmacy_dashboard.html', context)


   # <-- make sure this is the inlineformset_factory we defined


@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_dispense(request, emr_id):
    """
    Pharmacy staff can type any drug name, set qty & price, and generate a receipt.
    """
    emr = get_object_or_404(PatientEMR, pk=emr_id)

    # ------------------------------------------------------------------
    # 1. Prevent double-dispensing
    # ------------------------------------------------------------------
    if DispensedDrug.objects.filter(emr=emr).exists():
        messages.error(request, "This prescription has already been dispensed.")
        return redirect('pharmacy-dashboard')

    # ------------------------------------------------------------------
    # 2. Handle POST → Save drugs + create receipt
    # ------------------------------------------------------------------
    if request.method == 'POST':
        formset = DispenseDrugFormSet(request.POST, instance=emr)

        if formset.is_valid():
            # Save each drug (commit=False so we can set extra fields)
            dispensed_drugs = formset.save(commit=False)
            grand_total = 0

            for drug in dispensed_drugs:
                # Link to the current EMR & pharmacist
                drug.emr = emr
                drug.dispensed_by = request.user

                # Save to DB
                drug.save()

                # Add line total
                grand_total += drug.total()   # quantity * price_per_unit

            # ------------------------------------------------------------------
            # 3. Create the PharmacyReceipt
            # ------------------------------------------------------------------
            receipt = PharmacyReceipt.objects.create(
                patient=emr.patient,
                total_amount=grand_total,
                issued_by=request.user
            )
            receipt.dispensed_drugs.set(dispensed_drugs)

            messages.success(request, "Drugs dispensed – receipt generated!")
            return redirect('pharmacy-receipt-pdf', receipt.id)

        else:
            # If formset invalid, fall through to re-render with errors
            messages.error(request, "Please correct the errors below.")

    else:
        # GET request → fresh empty formset (3 blank rows)
        formset = DispenseDrugFormSet(instance=emr)

    # ------------------------------------------------------------------
    # 4. Render the page
    # ------------------------------------------------------------------
    context = {
        'emr': emr,
        'formset': formset,
    }
    return render(request, 'hospital/pharmacy_dispense.html', context)
# -------------------------------------------------------------------------
# PDF RECEIPT
# -------------------------------------------------------------------------
from django.shortcuts import get_object_or_404
from django.utils import formats
from decimal import Decimal

def pharmacy_receipt_pdf(request, receipt_id):
    receipt = get_object_or_404(PharmacyReceipt, pk=receipt_id)

    # Get dispensed drugs
    drugs = receipt.dispensed_drugs.all()

    context = {
        'receipt': receipt,
        'drugs': drugs,  # ← PASS DRUGS
        'patient': receipt.patient,
        'issued_by': receipt.issued_by.get_full_name() if receipt.issued_by else "Pharmacy",
        'date': receipt.issued_at.strftime("%d %B %Y"),
    }
    return render_to_pdf('hospital/pharmacy_receipt_pdf.html', context)


# -------------------------------------------------
# Send source billing items to Account department
# -------------------------------------------------
@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_send_to_account(request, receipt_id):
    receipt = get_object_or_404(PharmacyReceipt, pk=receipt_id)
    if request.method != 'POST':
        return redirect('pharmacy-receipt-detail', receipt_id=receipt.id)

    # Create a Bill (unassigned accountant) and a single BillItem referencing the receipt
    bill = models.Bill.objects.create(
        patient=receipt.patient,
        generated_by=None,
        status='pending',
        total_amount=0,
        discount=0,
        final_amount=0,
    )

    models.BillItem.objects.create(
        bill=bill,
        item_type='drug',
        description=f'Pharmacy Receipt #{receipt.id}',
        quantity=1,
        unit_price=receipt.total_amount,
        reference_id=str(receipt.id)
    )

    # Mark receipt as final and ensure totals are correct
    receipt.status = 'final'
    receipt.recalculate_total()
    receipt.save()

    messages.success(request, f'Receipt #{receipt.id} sent to Accounts.')
    return redirect('pharmacy-receipt-detail', receipt_id=receipt.id)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['LAB','DOCTOR']).exists())
def lab_send_to_account(request, result_id):
    result = get_object_or_404(LabResult, pk=result_id)
    if request.method != 'POST':
        return redirect('doctor-view-lab-results', patient_id=result.patient.id)

    # Default lab price; account generation UI uses 500 as default
    default_lab_price = getattr(settings, 'DEFAULT_LAB_PRICE', 500)

    bill = models.Bill.objects.create(
        patient=result.patient,
        generated_by=None,
        status='pending',
        total_amount=0,
        discount=0,
        final_amount=0,
    )

    models.BillItem.objects.create(
        bill=bill,
        item_type='lab',
        description=f'Lab Test: {result.test_name}',
        quantity=1,
        unit_price=default_lab_price,
        reference_id=str(result.id)
    )

    messages.success(request, f'Lab result "{result.test_name}" sent to Accounts.')
    return redirect('doctor-view-lab-results', patient_id=result.patient.id)

# ------------------------------------------------------------------
# PHARMACY - history, edit and delete dispensed drugs
# -----------------------------------------------------------------
@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_history(request):
    """
    Show list of all pharmacy receipts and allow quick search by patient.
    """
    q = request.GET.get('q')
    if q:
        receipts = PharmacyReceipt.objects.filter(patient__user__first_name__icontains=q).order_by('-issued_at')
    else:
        receipts = PharmacyReceipt.objects.all().order_by('-issued_at')
    return render(request, 'hospital/pharmacy_history.html', {'receipts': receipts})


@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_receipt_detail(request, receipt_id):
    receipt = get_object_or_404(PharmacyReceipt, pk=receipt_id)
    drugs = receipt.dispensed_drugs.all()
    return render(request, 'hospital/pharmacy_receipt_detail.html', {
        'receipt': receipt,
        'drugs': drugs,
    })


@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_edit_receipt(request, receipt_id):
    """
    Edit the dispensed drugs that belong to a specific receipt.
    Uses the inline formset bound to the parent EMR.
    """
    receipt = get_object_or_404(PharmacyReceipt, pk=receipt_id)
    # try to determine EMR from the dispensed drugs
    first_drug = receipt.dispensed_drugs.first()
    if not first_drug:
        messages.error(request, 'Receipt has no dispensed drugs to edit.')
        return redirect('pharmacy-history')

    emr = first_drug.emr

    # Limit the formset to only the dispensed drugs that belong to this receipt
    qs = DispensedDrug.objects.filter(pk__in=receipt.dispensed_drugs.values_list('pk', flat=True))
    formset = DispenseDrugFormSet(instance=emr, queryset=qs)

    if request.method == 'POST':
        formset = DispenseDrugFormSet(request.POST, instance=emr, queryset=qs)
        if formset.is_valid():
            saved = formset.save(commit=False)
            # Save and ensure dispensed_by / emr are set
            saved_pks = []
            for obj in saved:
                obj.emr = emr
                if not obj.dispensed_by:
                    obj.dispensed_by = request.user
                obj.save()
                saved_pks.append(obj.pk)

            # Handle deletions
            for obj in formset.deleted_objects:
                # remove from any receipts (including this one) and delete the record
                for r in PharmacyReceipt.objects.filter(dispensed_drugs=obj):
                    r.dispensed_drugs.remove(obj)
                    r.recalculate_total()
                obj.delete()

            # Update this receipt to point to the up-to-date set
            new_qs = DispensedDrug.objects.filter(pk__in=saved_pks)
            receipt.dispensed_drugs.set(new_qs)
            receipt.recalculate_total()
            messages.success(request, 'Receipt updated.')
            return redirect('pharmacy-receipt-detail', receipt_id=receipt.id)
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'hospital/pharmacy_edit_receipt.html', {
        'receipt': receipt,
        'formset': formset,
        'emr': emr,
    })


@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_edit_dispensed_drug(request, drug_id):
    drug = get_object_or_404(DispensedDrug, pk=drug_id)
    if request.method == 'POST':
        form = forms.DispenseDrugForm(request.POST, instance=drug)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dispensed_by = obj.dispensed_by or request.user
            obj.save()
            # Recalculate totals for receipts that include this drug
            for receipt in PharmacyReceipt.objects.filter(dispensed_drugs=obj):
                receipt.recalculate_total()
            messages.success(request, 'Drug updated')
            return redirect('pharmacy-receipt-detail', receipt_id=(PharmacyReceipt.objects.filter(dispensed_drugs=obj).first().id if PharmacyReceipt.objects.filter(dispensed_drugs=obj).exists() else ''))
    else:
        form = forms.DispenseDrugForm(instance=drug)
    return render(request, 'hospital/pharmacy_edit_dispensed_drug.html', {'form': form, 'drug': drug})


@login_required(login_url='pharmacy-login')
@user_passes_test(lambda u: u.groups.filter(name='PHARMACY').exists())
def pharmacy_delete_dispensed_drug(request, drug_id):
    drug = get_object_or_404(DispensedDrug, pk=drug_id)
    # Remember receipts for redirect
    receipts = list(PharmacyReceipt.objects.filter(dispensed_drugs=drug))
    if request.method == 'POST':
        # remove from receipts and recalc totals
        for r in receipts:
            r.dispensed_drugs.remove(drug)
            r.recalculate_total()
        drug.delete()
        messages.success(request, 'Drug removed from records')
        return redirect('pharmacy-history')

    return render(request, 'hospital/pharmacy_confirm_delete_drug.html', {'drug': drug, 'receipts': receipts})

# -------------------------------------------------------------------------
# LAB TECHNICIAN VIEWS
# -------------------------------------------------------------------------
@login_required(login_url='lab-login')
@user_passes_test(lambda u: u.groups.filter(name='LAB').exists())
def lab_dashboard(request):
    patients = Patient.objects.filter(status=True)
    return render(request, 'hospital/lab_dashboard.html', {'patients': patients})

@login_required(login_url='lab-login')
@user_passes_test(lambda u: u.groups.filter(name='LAB').exists())
def lab_add_result(request, request_id):
    from .forms import LabResultForm
    # REMOVE is_completed=False → allow viewing even if already done
    lab_request = get_object_or_404(LabRequest, pk=request_id)
    emr = lab_request.emr

    # Optional: Prevent double-entry
    if lab_request.is_completed:
        messages.error(request, "This lab request has already been completed.")
        return redirect('lab-pending-requests')

    if request.method == 'POST':
        form = LabResultForm(request.POST, lab_request=lab_request)
        if form.is_valid():
            result = form.save(commit=False)
            result.patient = emr.patient
            result.performed_by = request.user
            result.save()
            lab_request.is_completed = True
            lab_request.save()
            messages.success(request, f"Result saved for {result.test_name}")
            return redirect('lab-pending-requests')
    else:
        form = LabResultForm(lab_request=lab_request)

    return render(request, 'hospital/lab_add_result.html', {
        'form': form,
        'lab_request': lab_request,
        'patient': emr.patient,
    })

@login_required(login_url='doctor-login')
@user_passes_test(lambda u: u.groups.filter(name='DOCTOR').exists())
def doctor_view_lab_results(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    lab_results = LabResult.objects.filter(patient=patient).order_by('-performed_at')

    context = {
        'patient': patient,
        'lab_results': lab_results,
    }
    return render(request, 'hospital/doctor_lab_results.html', context)
def lab_report_pdf(request, result_id):
    result = get_object_or_404(LabResult, pk=result_id)
    return render_to_pdf('hospital/lab_report_pdf.html', {'result': result})
# In views.py
def lab_report_pdf(request, result_id):
    result = get_object_or_404(LabResult, pk=result_id)
    return render_to_pdf('hospital/lab_report_pdf.html', {'result': result})

def pharmacy_signup_view(request):
    userForm = forms.PharmacyUserForm()
    pharmacyForm = forms.PharmacyForm()
    if request.method == 'POST':
        userForm = forms.PharmacyUserForm(request.POST)
        pharmacyForm = forms.PharmacyForm(request.POST, request.FILES)
        if userForm.is_valid() and pharmacyForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            pharmacy = pharmacyForm.save(commit=False)
            pharmacy.user = user
            pharmacy.save()
            g, _ = Group.objects.get_or_create(name='PHARMACY')
            g.user_set.add(user)
            return redirect('pharmacy-login')
    return render(request, 'hospital/pharmacy_signup.html',
                  {'userForm': userForm, 'pharmacyForm': pharmacyForm})


def lab_signup_view(request):
    userForm = forms.LabUserForm()
    labForm = forms.LabForm()
    if request.method == 'POST':
        userForm = forms.LabUserForm(request.POST)
        labForm = forms.LabForm(request.POST, request.FILES)
        if userForm.is_valid() and labForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            lab = labForm.save(commit=False)
            lab.user = user
            lab.save()
            g, _ = Group.objects.get_or_create(name='LAB')
            g.user_set.add(user)
            return redirect('lab-login')
    return render(request, 'hospital/lab_signup.html',
                  {'userForm': userForm, 'labForm': labForm})

# -------------------------------------------------
# NURSE VIEWS
# -------------------------------------------------
def nurse_signup_view(request):
    userForm = forms.NurseUserForm()
    nurseForm = forms.NurseForm()
    if request.method == 'POST':
        userForm = forms.NurseUserForm(request.POST)
        nurseForm = forms.NurseForm(request.POST, request.FILES)
        if userForm.is_valid() and nurseForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            nurse = nurseForm.save(commit=False)
            nurse.user = user
            nurse.save()
            g, _ = Group.objects.get_or_create(name='NURSE')
            g.user_set.add(user)
            return redirect('nurse-login')
    return render(request, 'hospital/nurse_signup.html',
                  {'userForm': userForm, 'nurseForm': nurseForm})

@login_required(login_url='nurse-login')
@user_passes_test(lambda u: u.groups.filter(name='NURSE').exists())
def nurse_dashboard(request):
    patients = Patient.objects.filter(status=True)
    context = {
        'patients': patients,
        'nurse': models.Nurse.objects.get(user_id=request.user.id)
    }
    return render(request, 'hospital/nurse_dashboard.html', context)

@login_required(login_url='nurse-login')
@user_passes_test(lambda u: u.groups.filter(name='NURSE').exists())
def nurse_patient_list(request):
    patients = Patient.objects.filter(status=True)
    nurse = models.Nurse.objects.get(user_id=request.user.id)
    return render(request, 'hospital/nurse_patient_list.html', {
        'patients': patients,
        'nurse': nurse
    })

@login_required(login_url='nurse-login')
@user_passes_test(lambda u: u.groups.filter(name='NURSE').exists())
def nurse_add_vitals(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    nurse = models.Nurse.objects.get(user_id=request.user.id)
    
    if request.method == 'POST':
        form = forms.VitalSignsForm(request.POST)
        if form.is_valid():
            vitals = form.save(commit=False)
            vitals.patient = patient
            vitals.nurse = nurse
            vitals.save()
            messages.success(request, f"Vitals recorded for {patient.get_name}")
            return redirect('nurse-patient-list')
    else:
        form = forms.VitalSignsForm()

    return render(request, 'hospital/nurse_add_vitals.html', {
        'form': form,
        'patient': patient,
        'nurse': nurse
    })

@login_required(login_url='nurse-login')
@user_passes_test(lambda u: u.groups.filter(name='NURSE').exists())
def nurse_view_vitals(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    vitals = models.VitalSigns.objects.filter(patient=patient).order_by('-timestamp')
    nurse = models.Nurse.objects.get(user_id=request.user.id)
    
    return render(request, 'hospital/nurse_view_vitals.html', {
        'patient': patient,
        'vitals': vitals,
        'nurse': nurse
    })

# Enhance Doctor's view to see vitals
from django.db.models import Avg
from django.utils import timezone

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_vitals(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    vitals = models.VitalSigns.objects.filter(patient=patient).order_by('-timestamp')
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    
    # Get 30-day average vitals for this patient
    thirty_days_ago = timezone.now() - timedelta(days=30)
    avg_vitals = models.VitalSigns.objects.filter(
        patient=patient,
        timestamp__gte=thirty_days_ago
    ).aggregate(
        avg_temp=Avg('temperature'),
        avg_pulse=Avg('pulse_rate'),
        avg_resp=Avg('respiratory_rate'),
        avg_o2=Avg('oxygen_saturation')
    )
    
    return render(request, 'hospital/doctor_view_patient_vitals.html', {
        'patient': patient,
        'vitals': vitals,
        'doctor': doctor,
        'avg_vitals': avg_vitals
    })
# ------------------------------------------------------------------
# DOCTOR – view patient EMR (the view that was missing)
# ------------------------------------------------------------------
@login_required(login_url='doctor-login')
@user_passes_test(lambda u: u.groups.filter(name='DOCTOR').exists())
def doctor_emr_view(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    emr_records = PatientEMR.objects.filter(patient=patient).order_by('-date')
    context = {
        'patient': patient,
        'emr_records': emr_records,
    }
    return render(request, 'hospital/doctor_view_patient_emr.html', context)


# ------------------------------------------------------------------
# DOCTOR – view lab results for a patient
# ------------------------------------------------------------------
@login_required(login_url='doctor-login')
@user_passes_test(lambda u: u.groups.filter(name='DOCTOR').exists())
def doctor_view_lab_results(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    lab_results = LabResult.objects.filter(patient=patient).order_by('-performed_at')
    context = {
        'patient': patient,
        'lab_results': lab_results,
    }
    return render(request, 'hospital/doctor_lab_results.html', context)

# -------------------------------------------------
# ACCOUNT DEPARTMENT VIEWS
# -------------------------------------------------
def account_signup_view(request):
    userForm = forms.AccountUserForm()
    accountForm = forms.AccountForm()
    if request.method == 'POST':
        userForm = forms.AccountUserForm(request.POST)
        accountForm = forms.AccountForm(request.POST, request.FILES)
        if userForm.is_valid() and accountForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            account = accountForm.save(commit=False)
            account.user = user
            account.save()
            g, _ = Group.objects.get_or_create(name='ACCOUNT')
            g.user_set.add(user)
            return redirect('account-login')
    return render(request, 'hospital/account_signup.html',
                  {'userForm': userForm, 'accountForm': accountForm})

@login_required(login_url='account-login')
@user_passes_test(lambda u: u.groups.filter(name='ACCOUNT').exists())
def account_dashboard(request):
    # Show pending bills and recent transactions
    pending_bills = models.Bill.objects.filter(status='pending').order_by('-generated_at')
    recent_bills = models.Bill.objects.filter(status='paid').order_by('-generated_at')[:5]
    
    # Calculate totals
    today = timezone.now().date()
    today_total = models.Bill.objects.filter(
        status='paid', 
        generated_at__date=today
    ).aggregate(total=Sum('final_amount'))['total'] or 0
    
    context = {
        'pending_bills': pending_bills,
        'recent_bills': recent_bills,
        'today_total': today_total,
        'accountant': models.Account.objects.get(user_id=request.user.id)
    }
    return render(request, 'hospital/account_dashboard.html', context)

@login_required(login_url='account-login')
@user_passes_test(lambda u: u.groups.filter(name='ACCOUNT').exists())
def account_patient_list(request):
    patients = Patient.objects.filter(status=True)
    accountant = models.Account.objects.get(user_id=request.user.id)
    return render(request, 'hospital/account_patient_list.html', {
        'patients': patients,
        'accountant': accountant
    })

@login_required(login_url='account-login')
@user_passes_test(lambda u: u.groups.filter(name='ACCOUNT').exists())
def generate_bill(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    accountant = models.Account.objects.get(user_id=request.user.id)
    
    if request.method == 'POST':
        form = forms.BillForm(request.POST)
        formset = forms.BillItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            bill = form.save(commit=False)
            bill.patient = patient
            bill.generated_by = accountant
            bill.save()
            
            instances = formset.save(commit=False)
            for instance in instances:
                instance.bill = bill
                instance.save()
            
            bill.calculate_total()
            messages.success(request, 'Bill generated successfully.')
            return redirect('account-bill-detail', bill_id=bill.id)
    else:
        form = forms.BillForm()
        formset = forms.BillItemFormSet()
        
        # Pre-populate with pharmacy and lab charges
        pharmacy_receipts = models.PharmacyReceipt.objects.filter(
            patient=patient, 
            status='final'
        ).exclude(
            billitem__isnull=False
        )
        
        lab_results = models.LabResult.objects.filter(
            patient=patient
        ).exclude(
            billitem__isnull=False
        )
    
    return render(request, 'hospital/account_generate_bill.html', {
        'form': form,
        'formset': formset,
        'patient': patient,
        'accountant': accountant,
        'pharmacy_receipts': pharmacy_receipts,
        'lab_results': lab_results
    })

@login_required(login_url='account-login')
@user_passes_test(lambda u: u.groups.filter(name='ACCOUNT').exists())
def account_bill_detail(request, bill_id):
    bill = get_object_or_404(models.Bill, pk=bill_id)
    accountant = models.Account.objects.get(user_id=request.user.id)
    return render(request, 'hospital/account_bill_detail.html', {
        'bill': bill,
        'accountant': accountant
    })

@login_required(login_url='account-login')
@user_passes_test(lambda u: u.groups.filter(name='ACCOUNT').exists())
def mark_bill_as_paid(request, bill_id):
    if request.method == 'POST':
        bill = get_object_or_404(models.Bill, pk=bill_id)
        bill.status = 'paid'
        bill.save()
        messages.success(request, 'Bill marked as paid successfully.')
        return redirect('account-bill-detail', bill_id=bill.id)
    return redirect('account-dashboard')

@login_required(login_url='account-login')
@user_passes_test(lambda u: u.groups.filter(name='ACCOUNT').exists())
def account_discharge_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    accountant = models.Account.objects.get(user_id=request.user.id)
    
    # Calculate days spent
    days = (timezone.now().date() - patient.admitDate).days or 1
    
    if request.method == 'POST':
        form = forms.DischargeForm(request.POST)
        if form.is_valid():
            # Create discharge record
            discharge = models.PatientDischargeDetails.objects.create(
                patientId=patient.id,
                patientName=patient.get_name,
                assignedDoctorName=models.Doctor.objects.get(user_id=patient.assignedDoctorId).get_name,
                address=patient.address,
                mobile=patient.mobile,
                symptoms=patient.symptoms,
                admitDate=patient.admitDate,
                releaseDate=timezone.now().date(),
                daySpent=days,
                roomCharge=form.cleaned_data['room_charge'] * days,
                doctorFee=form.cleaned_data['doctor_fee'],
                medicineCost=models.PharmacyReceipt.objects.filter(
                    patient=patient,
                    status='final'
                ).aggregate(total=Sum('total_amount'))['total'] or 0,
                OtherCharge=form.cleaned_data['other_charges']
            )
            
            # Create final bill
            bill = models.Bill.objects.create(
                patient=patient,
                generated_by=accountant,
                status='pending',
                total_amount=0,  # Will be calculated after adding items
                discharge_summary=form.cleaned_data['discharge_summary']
            )
            
            # Add bill items
            items_to_create = [
                {
                    'item_type': 'room',
                    'description': f'Room Charges for {days} days',
                    'quantity': days,
                    'unit_price': form.cleaned_data['room_charge']
                },
                {
                    'item_type': 'doctor',
                    'description': 'Doctor Fee',
                    'quantity': 1,
                    'unit_price': form.cleaned_data['doctor_fee']
                }
            ]
            
            if form.cleaned_data['other_charges']:
                items_to_create.append({
                    'item_type': 'other',
                    'description': 'Other Charges',
                    'quantity': 1,
                    'unit_price': form.cleaned_data['other_charges']
                })
            
            # Create bill items
            for item in items_to_create:
                models.BillItem.objects.create(bill=bill, **item)
            
            # Add pharmacy charges
            for receipt in models.PharmacyReceipt.objects.filter(patient=patient, status='final'):
                models.BillItem.objects.create(
                    bill=bill,
                    item_type='drug',
                    description=f'Pharmacy Receipt #{receipt.id}',
                    quantity=1,
                    unit_price=receipt.total_amount,
                    reference_id=str(receipt.id)
                )
            
            bill.calculate_total()
            messages.success(request, 'Patient discharged successfully.')
            return redirect('account-bill-detail', bill_id=bill.id)
    else:
        form = forms.DischargeForm()
    
    return render(request, 'hospital/account_discharge_patient.html', {
        'form': form,
        'patient': patient,
        'accountant': accountant,
        'days_spent': days
    })
# hospital/views.py
# hospital/views.py

from .forms import PatientEMRForm, LabRequestFormSet  # ← ADD THIS

# hospital/views.py

# hospital/views.py

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_manage_emr(request, patient_id, emr_id=None):
    patient = get_object_or_404(models.Patient, pk=patient_id)
    doctor = models.Doctor.objects.get(user_id=request.user.id)

    if emr_id:
        emr = get_object_or_404(models.PatientEMR, pk=emr_id, patient=patient)
        action = "Edit"
    else:
        emr = models.PatientEMR(patient=patient, doctor=doctor)
        action = "Add"

    if request.method == 'POST':
        form = forms.PatientEMRForm(request.POST, instance=emr)
        lab_formset = forms.LabRequestFormSet(request.POST, instance=emr)

        if form.is_valid() and lab_formset.is_valid():
            # SAVE EMR FIRST
            emr_obj = form.save(commit=False)
            if not emr_obj.id:  # New EMR
                emr_obj.date = timezone.now()
            emr_obj.save()  # CRITICAL: SAVE HERE

            # SAVE LAB REQUESTS
            lab_requests = lab_formset.save(commit=False)
            for req in lab_requests:
                req.emr = emr_obj
                req.ordered_by = doctor.user
                req.save()
            for obj in lab_formset.deleted_objects:
                obj.delete()

            messages.success(request, f"EMR {action.lower()}ed successfully!")
            return redirect('doctor-view-patient-emr', patient_id=patient.id)
        else:
            # DEBUG: Show form errors
            print("EMR Form Errors:", form.errors)
            print("Lab Formset Errors:", lab_formset.errors)
    else:
        form = forms.PatientEMRForm(instance=emr)
        lab_formset = forms.LabRequestFormSet(instance=emr)

    context = {
        'form': form,
        'lab_formset': lab_formset,
        'patient': patient,
        'doctor': doctor,
        'action': action,
        'emr': emr if emr_id else None,
    }
    return render(request, 'hospital/doctor_manage_emr.html', context)

@login_required(login_url='lab-login')
@user_passes_test(lambda u: u.groups.filter(name='LAB').exists())
def lab_pending_requests(request):
    requests = LabRequest.objects.filter(is_completed=False).select_related('emr__patient')
    return render(request, 'hospital/lab_pending_requests.html', {'requests': requests})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_emr(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    emr_records = PatientEMR.objects.filter(patient=patient).order_by('-date')
    doctor = models.Doctor.objects.get(user_id=request.user.id)

    context = {
        'patient': patient,
        'emr_records': emr_records,
        'doctor': doctor,
    }
    return render(request, 'hospital/doctor_view_patient_emr.html', context)