from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('news', views.news, name='news'),
	path('tools', views.tools, name='tools'),
	path('tool_request', views.tool_request, name='tool_request'),
    path('frame_extract/', views.frame_extract, name='frame_extract'),
    path('frame_extract/frame_extract_download/', views.frame_extract_download, name='frame_extract_download'),
    path('generate_c_source/', views.generate_c_source, name='generate_c_source'),
]