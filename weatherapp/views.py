import requests
from django.shortcuts import render,redirect
#rom django.http import HttpResponseRedirect,HttpResponse
from .forms import CityForm
from weatherapp.models import City
from django.views.generic.edit import DeleteView
#from django.urls import reverse_lazyk


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=23d00bd37862920a212b3141bffbb412'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                err_msg = "City already exist in the database!"
        if err_msg :
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            message_class = "alert-success"
    
    print(err_msg)
    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for citi in cities:

        r = requests.get(url.format(citi)).json()
        city_weather  = {
            'city' : citi.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form':form,
        'message':message,
        'message_class':message_class
    }

    return render(request, 'weather.html',context)
def about(request) :
    return render(request,'about.html')

    
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

def help(request):
    return render(request,'help.html')
