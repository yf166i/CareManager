from . import views
from django.urls import path
from . import views

urlpatterns = [
    # アカウント
    path('signup/', views.signup_view, name='signup'),
    path('account/update/<int:pk>/', views.UserUpdate.as_view(), name='accountUpdate'),
    path('account/delete/<int:pk>/', views.UserDelete.as_view(), name='accountDelete'),
    # ログイン
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # 利用者
    path('user/index', views.Index.as_view(), name='index'),
    path('user/create', views.Create.as_view(), name='create'),
    path('user/update/<int:pk>/',views.Update.as_view(),name='update'),
    path('user/delete/<int:pk>/',views.Delete.as_view(),name='delete'),
    # 事例記録
    path('casereport/index', views.CaseReportIndex.as_view(), name='caseReportIndex'),
    path('casereport/create', views.CaseReportCreate.as_view(), name='caseReportCreate'),
    path('casereport/update/<int:pk>/',views.CaseReportUpdate.as_view(),name='caseReportUpdate'),
    path('casereport/delete/<int:pk>/',views.CaseReportDelete.as_view(),name='caseReportDelete'),
]