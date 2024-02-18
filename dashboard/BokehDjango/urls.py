from django.urls import path
from .views import stock_visualizations

app_name = "BokehDjango"
urlpatterns = [path("stock-visualizations/", stock_visualizations, name="stock-visualizations"),]