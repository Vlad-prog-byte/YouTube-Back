from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from MyTube import settings
from sitemy import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/register', views.SignupView.as_view()),
    path('api/csrf_cookie', views.GetCSRFToken.as_view()),
    path('authenticated', views.CheckAuthenticatedView.as_view()),
    path('auth/login', views.LoginView.as_view()),
    path('auth/logout', views.LogoutView.as_view()),
    path('auth/delete', views.DeleteAccountView.as_view()),
    path('profile/', views.GetUserProfileView.as_view()),
    path('users/', views.getUsers),
    path('search/', views.search),
    path('api/channel/<int:pk>', views.VideosChannelView.as_view()),
    path('api/likeDislike/delete', views.likeDislikeDelete.as_view()),
    path('api/likeDislike', views.likeDisLikesView.as_view()),
    path('api/newPhoto', views.newPhoto.as_view()),
    path('api/newVideo', views.newVideo.as_view()),
    path('api/manager/isPublished', views.IsPublishedVideo.as_view()),
    path('api/isPublished/delete', views.DeletePublishedVideo.as_view()),
    path('api/Accounts/delete', views.DeleteAccount.as_view())
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)