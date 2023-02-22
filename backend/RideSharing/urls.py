from django.urls import path
from . import views


urlpatterns = [
	#path('createuser/', views.createUser,name='Create_user'),
	#path('', views.index, name='index'),
	path('login', views.authenticateUser.as_view()),
	path('', views.userInformation.as_view()),# --> this handles all the get post put and delete request
	#path('users/', views.getUserInfo, name='Get_all_users'),
	path('users/<str:ph_number>', views.getOneUserInfo, name='Get_single_user_info'),
	path('lochi/<int:pk>', views.getLoci),
	path('update/<str:ph_number>', views.updateUser, name='Update_user_info'),
	path('delete/<str:ph_number>', views.deleteUser, name='delete_user'),

]

