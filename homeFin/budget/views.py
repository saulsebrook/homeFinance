from django.shortcuts import render
from . import excelData
from json import load
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


def budget(request):
    allocation = excelData.get_allocations()
    context = {
        'allocation': allocation,
    }

    return render(request, 'budget.html', context)

def income(request):
    income = excelData.get_income()
    context = {
        'income': income,
    }

    return render(request, 'income.html', context)

def presents(request):
    presents = excelData.get_presents_allocation()
    context = {
        'presents': presents,
    }

    return render(request, 'presents.html', context)

def change_salary(request):
    person = request.POST['person']
    newWage = request.POST['newWage']

    excelData.amend_wage(person, newWage)

    return HttpResponseRedirect(reverse('income'))

