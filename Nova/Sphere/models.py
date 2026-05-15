# Sphere/models.py
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    short_detail = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    meeting_link = models.URLField(blank=True, null=True) 
    registered = models.IntegerField(default=0)
    people_required = models.IntegerField()
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to="events/", blank=True, null=True)

    def __str__(self):
        return self.name
    def event_duration(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
    event_duration.short_description = "Duration"


    @property
    def verified_count(self):
        """Count only verified payments."""
        from Sphere.models import PaymentVerification
        return PaymentVerification.objects.filter(event=self, verified=True).count()

    @property
    def is_full(self):
        return self.verified_count >= self.people_required



class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.user.username} -> {self.event.name}"


class PaymentVerification(models.Model):
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15)
    verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.mpesa_code}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
# SwasTasks Models
class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    attachment = models.FileField(upload_to='task_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='bids')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'worker')  # one bid per worker per task

    def __str__(self):
        return f"{self.worker.username} bid on {self.task.title}"


class WorkSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='work_submissions/')
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.worker.username} submitted for {self.task.title}"