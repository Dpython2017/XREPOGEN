from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from . import views
urlpatterns = [
    url('^$', views.Dashboard.as_view(), name='index'),
    url('login/$', auth_view.LoginView.as_view(), name='login'),
    url('logout/$', auth_view.LogoutView.as_view(), name='logout'),
    url('fr/$',views.TemplateView.as_view(), name="formats_views"),
    url('formats_templates',views.ViewPics.as_view(),),
    url('create', views.CreateTemplate.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)