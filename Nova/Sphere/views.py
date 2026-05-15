from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, EventRegistration, PaymentVerification
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, PaymentVerificationForm
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from .stk_push import initiate_stk_push
from django.contrib.auth import login
from .forms import StudentRegistrationForm


# Core pages
def homepage(request):
    return render(request, 'Sphere/homepage.html')

def about(request):
    return render(request, 'Sphere/about.html')

def contact(request):
    return render(request, 'Sphere/contact.html')

# Solution pages
def IT_support(request):
    return render(request, 'Sphere/IT_support.html')

def software(request):
    return render(request, 'Sphere/software.html')

def hardware(request):
    return render(request, 'Sphere/hardware.html')

def networking(request):
    return render(request, 'Sphere/network.html')

def cybersec(request):
    return render(request, 'Sphere/cybersec.html')

def cloud(request):
    return render(request, 'Sphere/cloud.html')

def events(request):
    today = date.today()

    # Upcoming events (today or future)
    upcoming_events = Event.objects.filter(event_date__gte=today).order_by('event_date')

    # Past events (before today)
    past_events = Event.objects.filter(event_date__lt=today).order_by('-event_date')

    return render(request, "Sphere/events.html", {
        "events": upcoming_events,
        "past_events": past_events,
    })

def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.is_full:
        messages.error(request, "Sorry, this event is already full.")
        return redirect("events")

    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, "You are already registered for this event.")
        return redirect("events")

    
    EventRegistration.objects.create(event=event, user=request.user)

    messages.success(request, f"You have successfully registered for {event.name}! Please verify your payment.")
    return redirect("events")

def payment_instructions(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "Sphere/payment_instructions.html", {"event": event})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()  # save message to DB

            # Admin notification email
            subject = f"New Contact Message: {contact_message.subject}"
            body = f"""
            You have received a new message from {contact_message.name} ({contact_message.email}).

            Subject: {contact_message.subject}
            Message:
            {contact_message.message}
            """

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            # Confirmation email to user
            user_subject = "We Received Your Message - NovaSphere"
            user_body = f"""
            Hi {contact_message.name},

            Thank you for reaching out to us. We have received your message and will get back to you shortly.

            Your Message:
            {contact_message.message}

            Best regards,
            NovaSphere Team
            """

            send_mail(
                user_subject,
                user_body,
                settings.DEFAULT_FROM_EMAIL,
                [contact_message.email],
                fail_silently=False,
            )

            messages.success(request, " Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'Sphere/contact.html', {'form': form})


def verify_payment(request, event_id=None):
    # Get the specific event if provided in URL
    event = get_object_or_404(Event, id=event_id) if event_id else None

    # Fetch all events for dropdown
    all_events = Event.objects.all().order_by('event_date')

    if request.method == "POST":
        form = PaymentVerificationForm(request.POST)
        if form.is_valid():
            mpesa_code = form.cleaned_data['mpesa_code'].strip().upper()
            selected_event_id = request.POST.get("event_id")

            # Ensure an event is selected
            if not selected_event_id:
                messages.error(request, "Please select an event to verify payment for.")
                return redirect('verify_payment', event_id=event.id if event else all_events.first().id)

            selected_event = get_object_or_404(Event, id=selected_event_id)

            # Prevent duplicate M-Pesa submissions
            if PaymentVerification.objects.filter(mpesa_code=mpesa_code).exists():
                messages.error(request, "This M-Pesa code has already been submitted.")
                return redirect('verify_payment', event_id=selected_event.id)

            # Create record
            verification = form.save(commit=False)
            verification.event = selected_event
            verification.verified = False  # Manual admin verification
            verification.save()

            messages.success(request, "Payment submitted successfully! Check your email for the access link.")
            return redirect('verify_payment', event_id=selected_event.id)
        else:
            messages.error(request, "Please check your input and try again.")
    else:
        form = PaymentVerificationForm()

    return render(request, "Sphere/verify_payment.html", {
        "form": form,
        "event": event,
        "all_events": all_events,
    })


def pay_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == "POST":
        phone = request.POST.get("phone")
        user_id = request.user.id if request.user.is_authenticated else "Guest"

        if not phone:
            messages.error(request, "Please enter your phone number.")
            return redirect("pay_for_event", event_id=event.id)

        response = initiate_stk_push(
            phone=phone,
            amount=event.registration_fee,
            event_name=event.name,
            user_id=user_id
        )

        if "error" in response:
            messages.error(request, "Payment initiation failed. Try again.")
        else:
            messages.success(request, " Payment request sent. Check your phone simulator.")

        return redirect("pay_event", event_id=event.id)

    return render(request, "Sphere/pay_event.html", {"event": event})

#SWASTASKS VIEWS
# USER REGISTRATION 
from django.contrib.auth.decorators import login_required
from .models import Task, Bid, WorkSubmission

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in automatically
            messages.success(request, f"Welcome to NovaSphere, {user.username}!")
            return redirect('task_list')
    else:
        form = StudentRegistrationForm()
    return render(request, 'Sphere/register.html', {'form': form})

def task_list(request):
    tasks = Task.objects.filter(status='open').order_by('-created_at')
    return render(request, 'Sphere/task_list.html', {'tasks': tasks})


@login_required
def post_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        budget = request.POST.get('budget')
        deadline = request.POST.get('deadline')
        attachment = request.FILES.get('attachment')

        Task.objects.create(
            client=request.user,
            title=title,
            description=description,
            budget=budget,
            deadline=deadline,
            attachment=attachment,
        )
        messages.success(request, ' Task posted successfully!')
        return redirect('task_list')

    return render(request, 'Sphere/post_task.html')


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    bids = task.bids.all().order_by('-created_at')
    user_bid = bids.filter(worker=request.user).first()
    approved_bid = bids.filter(is_approved=True).first()
    user_submission = WorkSubmission.objects.filter(task=task, worker=request.user).first()

    return render(request, 'Sphere/task_detail.html', {
        'task': task,
        'bids': bids,
        'user_bid': user_bid,
        'approved_bid': approved_bid,
        'user_submission': user_submission,
    })


@login_required
def place_bid(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status != 'open':
        messages.error(request, 'This task is no longer accepting bids.')
        return redirect('task_detail', task_id=task.id)

    if Bid.objects.filter(task=task, worker=request.user).exists():
        messages.warning(request, ' You have already placed a bid on this task.')
        return redirect('task_detail', task_id=task.id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        message = request.POST.get('message')
        Bid.objects.create(task=task, worker=request.user, amount=amount, message=message)
        messages.success(request, ' Bid submitted! You will be notified if selected.')
        return redirect('task_detail', task_id=task.id)

    return redirect('task_detail', task_id=task.id)


@login_required
def approve_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    # Only the task's client can approve
    if request.user != bid.task.client:
        messages.error(request, 'You are not authorised to do this.')
        return redirect('task_detail', task_id=bid.task.id)

    # Approve this bid, reject all others
    bid.task.bids.update(is_approved=False)
    bid.is_approved = True
    bid.save()
    bid.task.status = 'assigned'
    bid.task.save()

    messages.success(request, f' {bid.worker.username} has been selected for this task!')
    return redirect('task_detail', task_id=bid.task.id)


@login_required
def submit_work(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    approved_bid = task.bids.filter(worker=request.user, is_approved=True).first()

    if not approved_bid:
        messages.error(request, 'You are not assigned to this task.')
        return redirect('task_detail', task_id=task.id)

    if request.method == 'POST':
        file = request.FILES.get('file')
        notes = request.POST.get('notes', '')

        if not file:
            messages.error(request, 'Please attach a file.')
            return redirect('task_detail', task_id=task.id)

        WorkSubmission.objects.create(task=task, worker=request.user, file=file, notes=notes)
        task.status = 'completed'
        task.save()
        messages.success(request, ' Work submitted successfully! Payment will be processed after review.')
        return redirect('task_detail', task_id=task.id)

    return redirect('task_detail', task_id=task.id)


@login_required
def my_dashboard(request):
    posted_tasks = Task.objects.filter(client=request.user).order_by('-created_at')
    my_bids = Bid.objects.filter(worker=request.user).order_by('-created_at')
    return render(request, 'Sphere/dashboard.html', {
        'posted_tasks': posted_tasks,
        'my_bids': my_bids,
    })