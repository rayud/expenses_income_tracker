from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from userincome import models 
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

sources = models.Source.objects.all()

def search_income(request) : 
    if request.method == 'POST' : 
        search_str = json.loads(request.body).get('searchText')
        income = models.UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | models.UserIncome.objects.filter(
            date__icontains=search_str, owner=request.user) | models.UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | models.UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user).order_by('-date')
        data = income.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request) : 
    
    preferences = UserPreference.objects.filter(user=request.user)[0].currency.split('-')[0].strip()
    income = models.UserIncome.objects.filter(owner=request.user).order_by('-date', 'amount')
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'income_list' : income,
        'page_obj': page_obj, 
        'currency' : preferences,
    }
    return render(request, 'income/index.html', context)

def add_income(request) : 
    context = {
        'sources' : sources,
        'values' : request.POST
    }

    if request.method == 'GET' : 
        return render(request,'income/add_income.html', context)
    if request.method == "POST": 
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']
        print(request.POST.items())
        models.UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
        messages.success(request, "Income Added Saved Successfully")
        return redirect('income')



def edit_income(request, id) : 
    income = models.UserIncome.objects.get(pk=id)
    context = {
        'income': income, 
        'values': income,
        'sources': sources, 
    }
    if request.method == 'GET' : 
        return render(request, 'income/edit_income.html', context)
    
    elif request.method == 'POST':

        income.owner = request.user
        income.amount = request.POST['amount']
        income.date = request.POST['date']
        income.source = request.POST['source']
        income.description = request.POST['description']
        income.save()
        messages.success(request, 'Updated successfully')
        return redirect('income')


def delete_income(request, id) : 
    income = models.UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request,'Income removed')
    return redirect('incomes')


def stats_view(request) : 
    return render(request, 'income/stats.html')

@login_required(login_url='/authentication/login')
def income_category_summary(request) : 
    today_date = datetime.date.today()
    six_months_ago = today_date - datetime.timedelta(days=180)
    income = models.UserIncome.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=today_date)
    finalrep = {}

    def get_source(individual_income) : 
        return individual_income.source
    category_list = list(set(map(get_source, income)))
     
    for i in income : 
        if i.source not in finalrep : 
            finalrep[i.source] = i.amount
        else : 
            finalrep[i.source] += i.amount
    
        

    return JsonResponse({'income_category_summary': finalrep
    }, safe=False)    


def export_csv(request) : 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=income' + \
        str(datetime.datetime.now())+ '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description','Source', 'Date'])

    income = models.UserIncome.objects.filter(owner=request.user)

    for inv_income in income : 
        writer.writerow([inv_income.amount, inv_income.description, inv_income.source,inv_income.date])

    return response


def export_excel(request) : 

    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=income' + str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0 

    font_style = xlwt.XFStyle()
    font_style.font.bold = True 

    columns = ['Amount', 'Description', 'Source', 'Date']

    for col_num in range(len(columns)) : 
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = models.UserIncome.objects.filter(owner=request.user).values_list(
        'amount', 
        'description', 
        'source', 
        'date'
    )
    for row in rows : 
        row_num += 1 
        for col_num in range(len(row)) : 
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response