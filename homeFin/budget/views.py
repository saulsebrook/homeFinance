from django.shortcuts import render
from . import excelData

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