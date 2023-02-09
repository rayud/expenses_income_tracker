from django.urls import path 
from userincome import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='income'), 
    path('add-income/', views.add_income, name="add-income"), 
    path('edit-income/<int:id>', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>', views.delete_income, name='delete-income'),
    path('search-incomes/', csrf_exempt(views.search_income), name='search_income'),
    path('income_category_summary/', views.income_category_summary, name="income_category_summary"),
    path('stats/', views.stats_view, name="income_stats"),
    path('export_csv/', views.export_csv, name="income_export_csv"), 
    path('export_excel/', views.export_excel, name="income_export_excel")
]