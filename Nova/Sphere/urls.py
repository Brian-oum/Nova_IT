from django.urls import path
from . import views

urlpatterns = [
    # Core pages
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),

    # Event actions
    path('events/register/<int:event_id>/', views.register_event, name='register_event'),
    path('payment/<int:event_id>/', views.payment_instructions, name='payment_instructions'),

    # Global verification page (user chooses event)
    path('event/<int:event_id>/verify/', views.verify_payment, name='verify_payment'),

    # Solution pages
    path('solutions/it-support/', views.IT_support, name='IT_support'),
    path('solutions/software-systems/', views.software, name='software'),
    path('solutions/hardware/', views.hardware, name='hardware'),
    path('solutions/networking/', views.networking, name='networking'),
    path('solutions/cybersec/', views.cybersec, name='cybersec'),
    path('solutions/cloud/', views.cloud, name='cloud'),
]
