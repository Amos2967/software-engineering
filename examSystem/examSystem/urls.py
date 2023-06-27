"""examSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from signUp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 默认访问首页
    url(r'^$', views.nindex),
    # 学生登陆
    url(r'^studentLogin/', views.studentLogin),
    # 教师登陆
    url(r'^teacherLogin/', views.teacherLogin),

    # 学生报名
    path('cet4/', views.cet4),  # 四级报名
    path('cet6/', views.cet6),  # 六级报名
    path('index/', views.index),
    path('register/', views.register,),

    # 缴费,废弃
    url(r'^QR_out/$', views.QR_out),

    # 考试界面
    url(r'^startExam/$', views.startExam),
    # 交卷后统计客观题成绩
    url(r'^calGrade/$', views.calGrade),
    # 查询学生信息
    url('queryStudent', views.queryStudent),
    # 登出
    url(r'^logout/$', views.logOut),
    # 教师批改主观题的目录
    url(r'^correSub/$', views.correSub),
    # 批改试卷的页面
    url(r'^mark/$', views.mark),

]
