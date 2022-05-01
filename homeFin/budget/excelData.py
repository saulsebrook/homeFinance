import openpyxl

budget = openpyxl.load_workbook('/Users/saulsebrook/Documents/Aulsebrook Budget.xlsx', data_only=True)

    
def get_allocations():  
    allocations = {}
    sheet = budget['Budget2022']
    x = list(sheet.columns)[9]
    y = list(sheet.columns)[8]
    for i in range(16, 31):
        allocations[y[i].value] = x[i].value
    
    return allocations

def get_income():
    income = {}
    sheet = budget['Budget2022']
    x = list(sheet.columns)[9]  
    y = list(sheet.columns)[8]
    for i in range(7, 9):
        income[y[i].value] = x[i].value
    
    return income

def get_presents_allocation():
    presents = {}
    sheet = budget['Budget2022']
    x = list(sheet.columns)[14]
    y = list(sheet.columns)[13]
    for i in range(7, 27):
        presents[y[i].value] = x[i].value
    
    return presents
i = get_allocations()
for x in i:
    print(x, i[x])