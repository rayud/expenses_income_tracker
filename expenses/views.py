from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from expenses import models 
from django.contrib import messages
from django.core.paginator import Paginator 
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference 
import datetime
import csv 
import xlwt
from django.http import FileResponse
import pdfkit
from django.template.loader import render_to_string


categories = models.Category.objects.all()

def search_expenses(request) : 
    if request.method == 'POST' : 
        search_str = json.loads(request.body).get('searchText')
        expenses = models.Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | models.Expense.objects.filter(
            date__icontains=search_str, owner=request.user) | models.Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | models.Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request) : 
    
    preferences = UserPreference.objects.filter(user=request.user)[0].currency.split('-')[0].strip()
    expenses = models.Expense.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'expenses_list' : expenses,
        'page_obj': page_obj, 
        'currency' : preferences,
    }
    return render(request, 'expense/index.html', context)

def add_expense(request) : 
    context = {
        'categories' : categories,
        'values' : request.POST
    }

    if request.method == 'GET' : 
        return render(request,'expense/add_expense.html', context)
    if request.method == "POST": 
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']
        print(request.POST.items())
        models.Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, "Expenses Added Saved Successfully")
        return redirect('expenses')



def edit_expense(request, id) : 
    expense = models.Expense.objects.get(pk=id)
    context = {
        'expense': expense, 
        'values': expense,
        'categories': categories, 
    }
    if request.method == 'GET' : 
        return render(request, 'expense/edit-expense.html', context)
    
    elif request.method == 'POST':

        expense.owner = request.user
        expense.amount = request.POST['amount']
        expense.date = request.POST['date']
        expense.category = request.POST['category']
        expense.description = request.POST['description']
        expense.save()
        messages.success(request, 'Updated successfully')
        return redirect('expenses')


def delete_expense(request, id) : 
    expense = models.Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,'Expense removed')
    return redirect('expenses')



@login_required(login_url='/authentication/login')
def expense_category_summary(request) : 
    today_date = datetime.date.today()
    six_months_ago = today_date - datetime.timedelta(days=180)
    expenses = models.Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=today_date)
    finalrep = {}

    def get_category(expense) : 
        return expense.category
    category_list = list(set(map(get_category, expenses)))
    
    for i in expenses : 
        print(i.category, i.amount, i.date)
    
    for i in expenses : 
        if i.category not in finalrep : 
            finalrep[i.category] = i.amount
        else : 
            finalrep[i.category] += i.amount
    
        

    return JsonResponse({'expense_category_summary': finalrep
    }, safe=False)


def stats_view(request) : 
    return render(request, 'expense/stats.html')


def export_csv(request) : 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expense' + \
        str(datetime.datetime.now())+ '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description','Catergory', 'Date'])

    expenses = models.Expense.objects.filter(owner=request.user)

    for expense in expenses : 
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response


def export_excel(request) : 

    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=Expense' + str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0 

    font_style = xlwt.XFStyle()
    font_style.font.bold = True 

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)) : 
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = models.Expense.objects.filter(owner=request.user).values_list(
        'amount', 
        'description', 
        'category', 
        'date'
    )
    for row in rows : 
        row_num += 1 
        for col_num in range(len(row)) : 
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response