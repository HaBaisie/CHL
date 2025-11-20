# hospitalmanagement/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from hospital import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ──────── HOME & STATIC ────────
    path('', views.home_view, name='home'),
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),

    # ──────── ROLE CLICKS ────────
    path('adminclick', views.adminclick_view, name='adminclick'),
    path('doctorclick', views.doctorclick_view, name='doctorclick'),
    path('patientclick', views.patientclick_view, name='patientclick'),

    # ──────── SIGNUP ────────
    path('adminsignup', views.admin_signup_view, name='adminsignup'),
    path('doctorsignup', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup', views.patient_signup_view, name='patientsignup'),
    path('pharmacy-signup', views.pharmacy_signup_view, name='pharmacy-signup'),
    path('lab-signup', views.lab_signup_view, name='lab-signup'),

    # ──────── LOGIN ────────
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html'), name='adminlogin'),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html'), name='doctorlogin'),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html'), name='patientlogin'),
    path('pharmacy-login', LoginView.as_view(template_name='hospital/pharmacy_login.html'), name='pharmacy-login'),
    path('lab-login', LoginView.as_view(template_name='hospital/lab_login.html'), name='lab-login'),

    # ──────── LOGOUT (ONLY ONE!) ────────
    path('logout', LogoutView.as_view(template_name='hospital/logout.html', next_page='home'), name='logout'),

    # ──────── AFTER LOGIN REDIRECT ────────
    path('afterlogin', views.afterlogin_view, name='afterlogin'),

    # ──────── ADMIN ────────
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-doctor', views.admin_doctor_view, name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view, name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view, name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view, name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view, name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view, name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view, name='reject-doctor'),
    path('admin-view-doctor-specialisation', views.admin_view_doctor_specialisation_view, name='admin-view-doctor-specialisation'),

    path('admin-patient', views.admin_patient_view, name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view, name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view, name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view, name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view, name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view, name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view, name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view, name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view, name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view, name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view, name='download-pdf'),

    path('admin-appointment', views.admin_appointment_view, name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view, name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view, name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view, name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view, name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view, name='reject-appointment'),

    # ──────── DOCTOR ────────
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('doctor-patient', views.doctor_patient_view, name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view, name='doctor-view-patient'),
    path('doctor-view-discharge-patient', views.doctor_view_discharge_patient_view, name='doctor-view-discharge-patient'),
    path('doctor-appointment', views.doctor_appointment_view, name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view, name='doctor-view-appointment'),
    path('doctor-delete-appointment', views.doctor_delete_appointment_view, name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view, name='delete-appointment'),
    path('doctor-view-patient-emr/<int:patient_id>/', views.doctor_view_patient_emr, name='doctor-view-patient-emr'),
    # path('doctor-add-emr/<int:patient_id>/', views.doctor_add_emr, name='doctor-add-emr'),
    path('doctor-emr-view/<int:patient_id>/', views.doctor_emr_view, name='doctor-emr-view'),
    path('doctor-view-lab-results/<int:patient_id>/', views.doctor_view_lab_results, name='doctor-view-lab-results'),

    # ──────── PATIENT ────────
    path('patient-dashboard', views.patient_dashboard_view, name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view, name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view, name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view, name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view, name='patient-discharge'),

    # ──────── PHARMACY ────────
    path('pharmacy-dashboard', views.pharmacy_dashboard, name='pharmacy-dashboard'),
    path('pharmacy-dispense/<int:emr_id>/', views.pharmacy_dispense, name='pharmacy-dispense'),
    path('pharmacy-receipt-pdf/<int:receipt_id>/', views.pharmacy_receipt_pdf, name='pharmacy-receipt-pdf'),
    path('pharmacy-history/', views.pharmacy_history, name='pharmacy-history'),
    path('pharmacy-receipt/<int:receipt_id>/', views.pharmacy_receipt_detail, name='pharmacy-receipt-detail'),
    # Send billing items to Account Dept
    path('pharmacy-send-to-account/<int:receipt_id>/', views.pharmacy_send_to_account, name='pharmacy-send-to-account'),
    path('pharmacy-receipt/<int:receipt_id>/edit/', views.pharmacy_edit_receipt, name='pharmacy-edit-receipt'),
    path('pharmacy/drug/<int:drug_id>/edit/', views.pharmacy_edit_dispensed_drug, name='pharmacy-edit-drug'),
    path('pharmacy/drug/<int:drug_id>/delete/', views.pharmacy_delete_dispensed_drug, name='pharmacy-delete-drug'),

    # ──────── LAB ────────
    path('lab-dashboard', views.lab_dashboard, name='lab-dashboard'),
    path('lab/add-result/<int:request_id>/', views.lab_add_result, name='lab-add-result'),
    path('lab-report-pdf/<int:result_id>/', views.lab_report_pdf, name='lab-report-pdf'),
    path('lab-send-to-account/<int:result_id>/', views.lab_send_to_account, name='lab-send-to-account'),

    # ──────── NURSE ────────
    path('nurse-signup', views.nurse_signup_view, name='nurse-signup'),
    path('nurse-login', LoginView.as_view(template_name='hospital/nurse_login.html'), name='nurse-login'),
    path('nurse-dashboard', views.nurse_dashboard, name='nurse-dashboard'),
    path('nurse-patient-list', views.nurse_patient_list, name='nurse-patient-list'),
    path('nurse-add-vitals/<int:patient_id>/', views.nurse_add_vitals, name='nurse-add-vitals'),
    path('nurse-view-vitals/<int:patient_id>/', views.nurse_view_vitals, name='nurse-view-vitals'),
    
    # Add vitals view to doctor's URLs
    path('doctor-view-patient-vitals/<int:patient_id>/', views.doctor_view_patient_vitals, name='doctor-view-patient-vitals'),

    # ──────── ACCOUNT DEPARTMENT ────────
    path('account-signup', views.account_signup_view, name='account-signup'),
    path('account-login', LoginView.as_view(template_name='hospital/account_login.html'), name='account-login'),
    path('account-dashboard', views.account_dashboard, name='account-dashboard'),
    path('account-patient-list', views.account_patient_list, name='account-patient-list'),
    path('account-generate-bill/<int:patient_id>/', views.generate_bill, name='account-generate-bill'),
    path('account-bill-detail/<int:bill_id>/', views.account_bill_detail, name='account-bill-detail'),
    path('account-discharge-patient/<int:patient_id>/', views.account_discharge_patient, name='account-discharge-patient'),
    path('account-mark-bill-paid/<int:bill_id>/', views.mark_bill_as_paid, name='account-mark-bill-paid'),

    # path('doctor/add-emr/<int:patient_id>/', views.doctor_add_emr, name='doctor-add-emr'),
    path('lab/pending/', views.lab_pending_requests, name='lab-pending-requests'),
    # hospital/urls.py
    path('doctor/emr/<int:patient_id>/', views.doctor_manage_emr, name='doctor-add-emr'),
    path('doctor/emr/<int:patient_id>/<int:emr_id>/', views.doctor_manage_emr, name='doctor-edit-emr'),
    
]
# THIS IS THE MAGIC THAT MAKES IMAGES APPEAR ON RENDER
if settings.DEBUG or getattr(settings, 'RENDER', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)