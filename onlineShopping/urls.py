"""
URL configuration for onlineShopping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from productCatalogue import views as pcViews
from registration import views as rgViews
from categoryMgt import views as categoryMgtViews
from shoppingCart import views as cartView

urlpatterns = [
    path('', pcViews.home),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', rgViews.signup, name='signup'),
    path('logout/', rgViews.redirectToHome),
    path('accounts/profile/', rgViews.redirectToHome),
    path('category/list/', categoryMgtViews.getCategory),
    path('category/create/', categoryMgtViews.create),
    path('category/update/<int:id>', categoryMgtViews.update),
    path("category/delete/<int:id>", categoryMgtViews.delete),
    path("category/", categoryMgtViews.getOurCategory),
    path('product/list/', pcViews.getProduct),
    path('product/create/', pcViews.create),
    path('product/update/<int:id>', pcViews.update),
    path("product/delete/<int:id>", pcViews.delete),
    path("product/detail/<str:slug>", pcViews.detail),
    path("cart/", cartView.cartView),
    path("checkout/", cartView.checkout),
    path("order-confirmation/", cartView.orderConfirmation),
    path("orders/", cartView.orders),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
