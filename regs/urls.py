from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .api import *
apipatterns = [
    path('news/', NewsAPI),
    path('news/id/', NewsByIdAPI),
    path('news/update/', NewsEditAPI),
    path('news/delete/', NewsDeleteAPI),
    path('news/create/', NewsCreateAPI),
    path('admins/', AdminsAPI)
]

urlpatterns = [
    path('', homepage, name = 'home'),
    path('api/', include(apipatterns)),
    path('about/', about, name = 'about'),
    path('register/', reg, name = 'register'),
    path('contact/', contact, name = 'contact'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('registration/<pk>/', reg_check, name = 'check_reg'),
    path('contact/<pk>/', check_con, name = 'check_con'),
    path('accounts/register/', register_account, name = 'account_register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'regs/log.html') , name = 'login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name = 'regs/logout.html') ,name = 'logout'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='regs/password_reset_form.html'), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='regs/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='regs/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='regs/password_reset_complete.html'), name = 'password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
