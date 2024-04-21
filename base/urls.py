from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.routing import websocket_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('user/', include('userauths.urls')),

    # Web Socket
    path("ws/", include(websocket_urlpatterns)),

    # Change Password
    path('user/change-password/', auth_views.PasswordChangeView.as_view(template_name='userauths/password-reset/change-password.html',
         success_url='/user/password-reset-complete/'), name='change_password'),
    path('user/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='userauths/password-reset/password_reset_complete.html'), name='password_reset_complete'),

    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
