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

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
