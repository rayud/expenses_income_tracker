from django.shortcuts import render
from django.conf import settings 
import json
# Create your views here.
from userpreferences import models 
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def index(request) : 
    
    currency_data = []
    file_path = settings.BASE_DIR / 'currencies.json'
    with open(file_path, 'r') as json_file : 
        data = json.load(json_file)
        for k,v in data.items() : 
            currency_data.append({'name':k, 'value': v})
    
    exists = models.UserPreference.objects.filter(user=request.user).exists()
    if exists : 
        user_preferences = models.UserPreference.objects.get(user=request.user)
    if request.method == 'POST' : 
        currency = request.POST['currency']
        if exists: 
            user_preferences.currency = currency
            user_preferences.save()
        else : 
            models.UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes Saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    else : 
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    