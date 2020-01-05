from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("product/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path('signup/', views.signup, name="signup1"),
    path('login/', views.login1, name="login"),
    path('logout/', views.logout1, name="logout"),
    path('track/', views.tracker, name="tracker"),
    path('hendlerequest/', views.hendlerequest, name="hendlerequest"),
]

