from django.urls import path

from authentication import views

urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('verify-email/', views.VerifyEmailApiView.as_view(), name='verify-email'),
    path('currencies', views.UpdateCurrenciesApiView.as_view(), name='update-currencies'),
    path('reset/', views.ResetPasswordAPIView.as_view(), name='reset'),
    path('reset_password/', views.ChangePasswordApiView.as_view(), name='reset-password'),
    path('reset_change_password/', views.SetNewPassword.as_view(), name='reset-change-password'),
]
