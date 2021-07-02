from django.urls import path
from . import views

urlpatterns=[
	path('',views.registerNew,name='registerNew'),
	path('login/', views.loginView, name="login"),
	path('about/',views.about,name="about"),  
	path('payment/',views.payment,name="payment"),
	path('contact/',views.contact,name="contact"),
    path('logout/', views.logoutUser, name="logout"), 
	path('trainer_register/',views.trainer_register,name="trainer_register"),
	path('member_register/',views.member_register,name="member_register"),
	path('dietician_register/',views.dietician_register,name="dietician_register"),
	path('profile_trainer/trainer_detail/',views.trainer_detail,name="trainer_detail"),
	path('profile_member/member_detail/',views.member_detail,name="member_detail"),
	path('profile_dietician/dietician_detail/',views.dietician_detail,name="dietician_detail"),
	path('profile_trainer/edit_profile_trainer/',views.edit_profile_trainer,name="edit_profile_trainer"),
	path('profile_member/edit_profile_member/',views.edit_profile_member,name="edit_profile_member"),
	path('profile_dietician/edit_profile_dietician/',views.edit_profile_dietician,name="edit_profile_dietician"),
	path('profile_trainer/',views.profileTrainer,name="profile_trainer"),
	path('profile_member/',views.profileMember,name="profile_member"),
	path('profile_dietician/',views.profileDietician,name="profile_dietician"),
	path('trainer_list/',views.trainer_list,name="trainer_list"),
	path('dietician_list/',views.dietician_list,name="dietician_list"),
	path('trainer/<slug:my_name>',views.dynamic_lookup,name="dynamic_lookup"),
	path('dietician/<slug:my_name>',views.dynamic_lookup_dietician,name="dynamic_lookup_dietician"),
	path('profile_member/trainers_list/trainer_book/<slug:my_name>',views.bookslot,name="bookslot"),
	path('profile_member/dieticians_list/dietician_book/<slug:my_name>',views.bookslot_dietician,name="bookslot_dietician"),
	path('profile_trainer/bookings/',views.bookings,name="bookings")
]