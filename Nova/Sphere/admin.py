from django.contrib import admin
from .models import Event, PaymentVerification
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# --- Inline for Event page ---
class PaymentVerificationInline(admin.TabularInline):
    model = PaymentVerification
    extra = 0
    fields = ('full_name', 'email', 'mpesa_code', 'verified', 'timestamp')
    readonly_fields = ('timestamp',)
    show_change_link = True


# --- Event Admin ---
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_date", "event_duration", "location", "registered", "people_required")
    list_filter = ("event_date", "location")
    search_fields = ("name", "location")
    ordering = ("event_date",)
    inlines = [PaymentVerificationInline]


# --- Payment Verification Admin ---
@admin.register(PaymentVerification)
class PaymentVerificationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'event', 'mpesa_code', 'verified', 'timestamp')
    list_filter = ('verified', 'event')
    search_fields = ('mpesa_code', 'phone_number', 'full_name', 'email')
    ordering = ('-timestamp',)

    def save_model(self, request, obj, form, change):
        was_verified = False
        if change:
            previous = PaymentVerification.objects.get(pk=obj.pk)
            was_verified = previous.verified

        super().save_model(request, obj, form, change)

        # ✅ When verification changes from False → True
        if obj.verified and not was_verified:
            event = obj.event

            # ✅ Safely increase slot count
            if event.registered < event.people_required:
                event.registered += 1
                event.save()

            # ✅ Send access email
            try:
                send_mail(
                    subject=f"Access Link for {event.name}",
                    message=(
                        f"Hello {obj.full_name},\n\n"
                        f"Your payment for '{event.name}' has been verified successfully.\n\n"
                        f"Join here: {event.meeting_link if event.meeting_link else event.location}\n\n"
                        f"Thank you for registering!\n"
                        f"NovaSphere IT Solutions Ltd"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )
                messages.success(request, f"✅ Email sent to {obj.full_name}.")
            except Exception as e:
                messages.error(request, f"❌ Failed to send email: {e}")
