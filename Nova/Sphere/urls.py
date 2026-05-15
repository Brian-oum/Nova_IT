from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Core pages
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),

    # Event actions
    path('events/register/<int:event_id>/', views.register_event, name='register_event'),
    path('payment/<int:event_id>/', views.payment_instructions, name='payment_instructions'),
    path("pay/<int:event_id>/", views.pay_event, name="pay_event"),

    # Global verification page (user chooses event)
    path('event/<int:event_id>/verify/', views.verify_payment, name='verify_payment'),

    # Solution pages
    path('solutions/it-support/', views.IT_support, name='IT_support'),
    path('solutions/software-systems/', views.software, name='software'),
    path('solutions/hardware/', views.hardware, name='hardware'),
    path('solutions/networking/', views.networking, name='networking'),
    path('solutions/cybersec/', views.cybersec, name='cybersec'),
    path('solutions/cloud/', views.cloud, name='cloud'),


    #SWAS Tasks paths
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/post/', views.post_task, name='post_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/bid/', views.place_bid, name='place_bid'),
    path('bid/<int:bid_id>/approve/', views.approve_bid, name='approve_bid'),
    path('tasks/<int:task_id>/submit/', views.submit_work, name='submit_work'),
    path('dashboard/', views.my_dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='Sphere/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
]