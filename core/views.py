from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .forms import AppointmentForm, ContactForm, UserForm, EditProfileForm
from .models import Department, Doctor
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


#  Registration Function
def register_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Hash the password
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Invalid data! Please check your inputs.")
    else:
        form = UserForm()

    return render(request, "core/register.html", {"form": form})


# 🔹 Login Authentication
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect("login")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("index")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "core/login.html")


#  Logout Function
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")


#  Profile View
@login_required(login_url="login")
def profile_view(request):
    return render(request, "core/profile.html")


#  Update the profile
def update_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "You're profile has updated successfully!")
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    context = {"form": form}
    return render(request, 'core/update-profile.html', context)


#  Index View (Loads homepage with dynamic data)
def index_view(request):
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    form = AppointmentForm()
    contact_form = ContactForm()

    return render(
        request,
        "core/index.html",
        {
            "form": form,
            "doctors": doctors,
            "departments": departments,
            "contact_form": contact_form,
        },
    )


#  Appointment Function
@login_required(login_url="login")
def appointment_view(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            try:
                appointment.date = datetime.strptime(
                    str(appointment.date), "%Y-%m-%d"
                ).date()
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return redirect("index")

            appointment.save()

            user_email = appointment.email

            try:
                send_mail(
                    subject="Appointment Confirmation",
                    message=f"Dear {appointment.name},\n\nYour appointment for {appointment.department} with {appointment.doctor} on {appointment.date} has been confirmed.\n\nThank you!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=False,
                )

                messages.success(
                    request,
                    "Your appointment has been booked successfully. A confirmation email has been sent.",
                )
            except Exception as e:
                messages.error(request, f"Email failed to send: {str(e)}")

            return redirect("index")

        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field.capitalize()}: {', '.join(errors)}")

            return redirect("index")

    messages.error(request, "Invalid request method.")
    return redirect("index")


#  Load Doctors Based on Selected Department (AJAX)
@login_required(login_url="login")
def load_doctors(request):
    department_id = request.GET.get("department")
    doctors = Doctor.objects.filter(department_id=department_id)

    doctor_data = [
        {
            "id": doctor.id,
            "name": doctor.name,
            "bio": doctor.bio,
            "doctor_image": doctor.doctor_image.url if doctor.doctor_image else None,
        }
        for doctor in doctors
    ]

    return JsonResponse(doctor_data, safe=False)


#  Contact Form View
@login_required(login_url="login")
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            subject = f"New Contact Inquiry: {contact.subject}"
            body = f"""
                Name: {contact.name}
                Email: {contact.email}
                Subject: {contact.subject}
                Message: {contact.message}
            """

            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, f"Email failed to send: {str(e)}")

            return redirect("index")

    messages.error(request, "Invalid form submission. Please check your inputs.")
    return redirect("index")
