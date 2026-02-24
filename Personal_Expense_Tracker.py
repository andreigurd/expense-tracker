
from tabulate import tabulate
import json
import csv
import os
from colorama import Fore, Style, init

#-----------------------------------------------------------------------
#   opening expenses json file
#-----------------------------------------------------------------------
try:
    with open('expenses.json', 'r') as file:
        expenses = json.load(file)
except FileNotFoundError:
    print("Expenses file not found. Blank list created.")
    expenses = [] # makes an empty list
except json.JSONDecodeError:
    print("Issue loading Expenses file. File empty or invalid JSON file. Blank Expenses list created.")
    expenses = []
except ValueError:
    print("Invalid expense item. Blank list created.")
    expenses = []
except PermissionError:
    print("Need permission to access Expenses file. Blank Expenses list created.")
    expenses = []

#-----------------------------------------------------------------------
#   opening budget json file
#-----------------------------------------------------------------------
try:
    with open('budgets.json', 'r') as file:
        budgets = json.load(file)
except FileNotFoundError:
    print("Budgets file not found. Blank list created.")
    budgets = []
except json.JSONDecodeError:
    print("Issue loading Budgets file. File empty or invalid JSON file. Blank Budgets list created.")
    budgets = []
except ValueError:
    print("Invalid budget item. Blank list created.")
    budgets = []
except PermissionError:
    print("Need permission to access Budgets file. Blank Budgets list created.")
    budgets = []

#-----------------------------------------------------------------------
#   opening savings goal json file
#-----------------------------------------------------------------------
try:
    with open('saving_goals.json', 'r') as file:
        saving_goals = json.load(file)
except FileNotFoundError:
    print("Goals file not found. Goal set to default zero.")
    saving_goals = {"month_goal": 0}
except json.JSONDecodeError:
    print("Issue loading Goals file. File empty or invalid JSON file. Goal set to default zero.")
    saving_goals = {"month_goal": 0}
except ValueError:
    print("Invalid Goals item. Goal set to default zero.")
    saving_goals = {"month_goal": 0}
except PermissionError:
    print("Need permission to access Goals file. Goal set to default zero.")
    saving_goals = {"month_goal": 0}

#-----------------------------------------------------------------------
#   timestamp
#-----------------------------------------------------------------------

from datetime import datetime
def datetime_now_stamp():    
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_string

# importing time delta to allow time change functions
from datetime import datetime,timedelta

#-----------------------------------------------------------------------
#   showing menu
#-----------------------------------------------------------------------

def show_menu():
    print("")
    print("Welcome to Expense Tracker!")
    print("[0] Exit")
    print("[1] Add Expense")
    print("[2] View All Expenses")
    print("[3] View Total")
    print("[4] View By Category")    
    print("[5] Search Expenses")
    print("[6] View Range")
    print("[7] Delete an Expense")
    print("[8] Set Category Budget")
    print("[9] View Category Budget Stats")
    print("[10] Monthly Saving Goals")
    print("[11] View Monthly Report")
    print("[12] View Spending Trend")
    print("[13] Export expenses to CSV")    

#-----------------------------------------------------------------------
#   option [1] Add Expense
#-----------------------------------------------------------------------
def add_expense():   
    while True:        
        try:
            amount = float(input("Enter the amount: "))
            break          
        except ValueError:
            print("Invalid number. Please try again.")

# note valid answers should be case sensive of how we want stored. user input can be converted.
    valid_category = ["food", "transport", "entertainment", "bills", "other"]
    while True:
        #.lower() converts input to lower case.
        category = input("Enter category (Food, Transport, Entertainment, Bills, Other): ").lower()
        if category in valid_category:
            break
        else:
            print("Invalid Category. Please try again.")

    description = input("Enter description: ")    

    #make gen expense dictionary
    # dont capitalize keys here to display them capitalized in table. otherwise the terms will have to be capilized everywhere.
    expense_item = {
        "date": datetime_now_stamp(),
        "amount": amount,
        "category": category,
        "description": description        
    }

    #list apend dictionary into list.
    expenses.append(expense_item)    
    print(f"Added expense: ${amount} under '{category}' category.")
    
#-----------------------------------------------------------------------
#   option [2] View All Expenses
#-----------------------------------------------------------------------
def view_expenses():
    
    print("Your Expenses:")      
    print(tabulate(expenses,headers="keys", tablefmt="grid"))
    
#-----------------------------------------------------------------------
#   option [3] View Total
#-----------------------------------------------------------------------
def add_up_expenses():
    #print("Total Expenses Amount")
    total_expenses = sum(expense["amount"] for expense in expenses)    
    #print("${:.2f}".format(total_expenses))
    return(total_expenses)
    
#-----------------------------------------------------------------------
#   option [4] View All Time Totals By Category
#-----------------------------------------------------------------------
# use the track totals per category function when activated in option 4
def view_categories():
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        if category in category_totals:
            category_totals[category] += expense['amount']
        else:
            category_totals[category] = expense['amount']

    cat_totals_list = []
    for category, total in category_totals.items():
        cat_totals_list.append([category, total]) 

    total_expenses = sum(expense["amount"] for expense in expenses)
    # adding a totals row
    cat_totals_list.append(["total", total_expenses])
    
    # note tabulate works for lists or multiple dictionaries. doesnt work with one dictionary.
    headers = ["Category","Totals"] #note this is display headers so they do not have to match previous category key refrenced with lower case.

    # note the list created appended items as one list (category, total). can define headers here because there are no key now.
    print(tabulate(cat_totals_list,headers = headers, tablefmt="grid")) #note headers can just be replaced with ["Category","Totals"] here
    write_json()    


#-----------------------------------------------------------------------
#  option [5] Search by description term
#-----------------------------------------------------------------------
# menue item search triggers a function. asks user for search term. creates a temp list in function based on that term and displays a table with results.
def search_expenses():
    search_term = input("Enter description search term: ").lower()

    searched_list = [expense for expense in expenses if search_term in expense['description'].lower()]   
    #print(searched_list)    
    print(tabulate(searched_list,headers = "keys", tablefmt="grid"))
    write_json()

#-----------------------------------------------------------------------
#   option [6] View last [x] days
#-----------------------------------------------------------------------

def view_recent():
    while True:        
        try:
            input_days = int(input("Select Number of Days in Range: "))
            print(f" {input_days} Day(s) Selected.")
            break
                    
        except ValueError:
            print("Invalid entry. Please try again.")

    recent = []
    for expense in expenses:
        expense_date = datetime.strptime(expense['date'], "%Y-%m-%d %H:%M:%S")
        cutoff = datetime.now() - timedelta(days=input_days)
        
        if expense_date >= cutoff:
            recent.append(expense)

#need to add up those recent expenses and add total to list and table    
    recent_total = (sum(expense["amount"] for expense in recent))
    
    recent_total_dict = {"date":'total',"amount":recent_total,"category":"","description":""}
    recent.append(recent_total_dict)
    
    #print(recent)
    print(tabulate(recent,headers = "keys", tablefmt="grid"))
    write_json()

#-----------------------------------------------------------------------
#   option [7] Delete an Expense
#-----------------------------------------------------------------------
def delete_expense():    
    print("Displaying all Expenses")    
    numbered_list = []    
    for number, expense in enumerate(expenses, start=1): #enumerate starts at 0 but lenght does not so need -1 to correct. (enumerate(list, start=1)))
        numbered_expenses = {
            "number": number,
            "date": expense['date'],
            "amount": expense['amount'],
            "category": expense['category'],
            "description": expense['description']
            }
                
        numbered_list.append(numbered_expenses)

    print(tabulate(numbered_list,headers = "keys", tablefmt="grid"))
        
    removed_expense_list = []
    while True:        
        try:
            choice = int(input("Select Expense Number to Delete: "))
            if 1<=choice<= len(expenses): #note enumerate starts at 0 but lenght does not so need -1 to correct. unless enumerate start=1
                print(f"Expense Number {choice} deleted.")
                #print(expenses[choice-1])
                removed_expense = expenses.pop(choice-1)   #list still starts with 0 even if enumerate was directed to start with 1
                removed_expense_list.append(removed_expense)                               
                print(tabulate(removed_expense_list,headers = "keys", tablefmt="grid"))
                write_json()
                break
            else:
                print("Number out of range. Please try again.")           

        except ValueError:
            print("Invalid entry. Please try again.")

#-----------------------------------------------------------------------
#   option [8] Set Category Monthly Budget
#-----------------------------------------------------------------------

def set_category_budget():

    print("Current Budgets")
    print(tabulate(budgets,headers = "keys", tablefmt="grid"))    
    
    valid_category = ["food", "transport", "entertainment", "bills", "other"]
# note to avoid loops inside loops
    while True:  
        category = input("Enter budget category (Food, Transport, Entertainment, Bills, Other): ").lower()
        if category in valid_category:
            break    # note return would stop the rest of the function.                            
        else:
            print("Invalid category. Please try again.")

# check if budget exists to avoid duplicates. 

    flag = None
    for budget in budgets:              
                if budget["category"] == category:
                    flag = budget
                    break                   

# overide or use existing budget.
    
    if flag:
        print(f" A monthly budget of ${flag['amount']} already exists for {category} category.")
        while True:
            answer = input("Override or Continue with amount?: ").lower()

            if answer == "override":
                budgets.remove(flag) 
        
                break # return here would skip next loop of adding amount.

                    
            elif answer == "continue":
                return
    
            else:
                print("Invalid option. Please try again.")
        

# input budget amount 
    while True:        
        try:
            amount = float(input("Enter monthly budget amount: "))
            print(f" ${amount} budget entered in {category} category.")
            break            

        except ValueError:
            print("Invalid number. Please try again.")

    cat_budget = {      
        "category": category,
        "amount": amount              
    }
    
    budgets.append(cat_budget)  
        
    write_budget_json()

#-----------------------------------------------------------------------
#   function to put current months expenses in a list
#----------------------------------------------------------------------- 
def current_month_expenses(): 
    month_expenses = []
    for expense in expenses:
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")       
    
        expense_date = (expense['date'])[:7]              
        month_now = date_string[:7]

        if expense_date == month_now:
            month_expenses.append(expense)
    return month_expenses

#-----------------------------------------------------------------------
#   function to get current months expenses totals
#----------------------------------------------------------------------- 
def category_totals():      
    month_expenses = current_month_expenses()
    #gives month_expenses list []

    month_category_totals = {}
    for expense in month_expenses:
        category = expense['category']
        if category in month_category_totals:
            month_category_totals[category] += expense['amount']            
        else:
            month_category_totals[category] = expense['amount']
    return month_category_totals
            
        

#-----------------------------------------------------------------------
#   option [9] View Category Monthly Budget
#-----------------------------------------------------------------------        
def view_category_budget():
    print("Monthly Budget Stats")      
    month_expenses = current_month_expenses()
    # gives month_expenses list []

    month_category_totals = category_totals()
    #gives month_category_totals dict {}

    all_category = ["food", "transport", "entertainment", "bills", "other"]
            
    budget_stats = []  
    for category in all_category:
        spent = month_category_totals.get(category, 0)
        budget = 0
        for item in budgets:
            if item['category'] == category:
                budget = item['amount']
                break
                
        if budget == 0:
            stats_dict = {
        "category" : category,
        "budget" : "No Budget", 
        "spent" : spent,    
        "remaining" : "N/A",
        "perc used" : "N/A",
        "status" : "N/A"
        }
        else:
            stats_dict = {
        "category" : category,
        "budget" : f"${budget:.2f}", 
        "spent" : f"${spent:.2f}",    
        "remaining" : f"${budget - spent if budget else 0:.2f}",
        "perc used" : f"{(spent / budget)*100 if budget else 0:.0f}%",
        "status" : "✅" if spent < budget else "⚠️"
        }
            
        budget_stats.append(stats_dict)           
    return(budget_stats)
    

#-----------------------------------------------------------------------
#   calculate and display savings goal status
#----------------------------------------------------------------------- 
def display_savings_goal_status():
    month_expenses = current_month_expenses()
    total_spent = sum(expense["amount"] for expense in month_expenses)

    current_goal = saving_goals["month_goal"]

    print("Monthly Savings Goal Status")

    if current_goal == 0:
        print("No savings goal set.")
        return
    
    # return ends function if no goal
    
    remaining = current_goal - total_spent
    print(f'Amount spent this month: ${total_spent:.2f}')

    if remaining > 0:
        print(Fore.GREEN + f'✅  Great job. Spending is ${remaining:.2f} under budget.' + Style.RESET_ALL)
    else:
        print(Fore.RED + f'⚠️  You have some improving to do. Spending is ${remaining:.2f} over budget.' + Style.RESET_ALL)



#-----------------------------------------------------------------------
#   option [10] monthly savings goals
#----------------------------------------------------------------------- 
# default saving_goals = [] list made at the top

def set_saving_goals():

    # display goal status
    display_savings_goal_status()

    current_goal = saving_goals["month_goal"]

    # if goal exists ask questions
    if saving_goals["month_goal"] > 0:
        print(f'Current monthly saving goal is ${current_goal:.2f}')

        while True:            
            answer = input("Override or Continue with goal?: ").lower()

            if answer == "override":
                saving_goals.clear()
                break
            elif answer == "continue":
                return
            else:
                print("Invalid option. Please try again.")    
    
    # input savings goal amount 
    while True:        
        try:
            saving_goals["month_goal"] = float(input("Enter monthly saving goal: "))
            print(f' ${saving_goals["month_goal"]} goal entered.')
            break            

        except ValueError:
            print("Invalid number. Please try again.")

    write_savings_json()

    # display new goal status
    display_savings_goal_status()

#-----------------------------------------------------------------------
#   option [11] View monthly report
#-----------------------------------------------------------------------  
def monthly_report():
    month_expenses = current_month_expenses()
    #gives month_expenses list []

    if month_expenses:
        pass
    else:
        print("No expenses this month")
        return

    month_category_totals = category_totals()
    #gives month_category_totals dict {}
    
    total_expenses = sum(expense["amount"] for expense in month_expenses)

    number_of_expenses = len(month_expenses)

    average_expense = total_expenses / number_of_expenses

    # note .sort re revises the original list/dict accending. sorted returns a new list.
    
    sorted_expenses = sorted(expenses, key=lambda expense: expense["amount"], reverse=True)
    #print(sorted_expenses)

    all_category = ["food", "transport", "entertainment", "bills", "other"]
    
    expense_stats = {
    "total spent" : f"${total_expenses:.2f}",
    "number of expenses": number_of_expenses,
    "average per expense": f"${average_expense:.2f}"
}
    
    expense_stats_list = []
    for key, value in expense_stats.items():
        expense_stats_list.append([key, value]) 

    headers = ["Current Month Expenses",""]
            
    print(tabulate(expense_stats_list,headers = headers, tablefmt="grid"))       

#-----------------------------------------------------------------------  
    print("")
    print("Category Totals and Percentages of Total Spent")
    
    category_stats = []  
    for category in all_category:                    
        total_spent = month_category_totals.get(category, 0)
        stats_dict = {
            "category" : category,        
            "total spent" : total_spent,           
            "perc of total" : f"{(total_spent/total_expenses)*100 if total_expenses else 0:.0f}%"        
        }       

        category_stats.append(stats_dict)           

    print(tabulate(category_stats,headers = "keys", tablefmt="grid"))                       

    #-----------------------------------------------------------------------
    top_expenses = sorted_expenses[0:5]
    print("")
    print("Top 5 Expenses")
    print(tabulate(top_expenses,headers = "keys", tablefmt="grid"))              
            
    write_json()

#-----------------------------------------------------------------------
#   option [12] View spending trend
#-----------------------------------------------------------------------  
def run_spending_trend():
    
    expense_months = []
    for expense in expenses:
        expense_date = (expense["date"])[:7]
        months_dict = {"date" : expense_date}
        expense_months.append(expense_date)    
    
    unique_months = sorted(set(expense_months))

    print("")
    print("Spending Trend")

    spending_trend = []
    for month in unique_months:        
        month_total = sum(expense_item["amount"] for expense_item in expenses if month == expense_item["date"][:7])
        
        increment = int(month_total/50)
        bar = ("█")*increment

        trend = {
            "year-month" : month,
            "total" : f"${month_total:.2f}",
            "trend (each represents $50)" : bar
        }
        spending_trend.append(trend)    
    
    print(tabulate(spending_trend,headers = "keys", tablefmt="grid"))      


#-----------------------------------------------------------------------
#   option [13] CSV export expenses
#-----------------------------------------------------------------------  
def csv_export():

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")     
    date_now = date_string[:10]

    with open(f'{date_now} expenses.csv', 'w') as file:
        file.write("Date,Amount,Category,Description\n")
        for expense in expenses:
            file.write(f"{expense['date']},{expense['amount']},{expense['category']},{expense['description']}\n")
    
    file_path = os.path.abspath(f'{date_now} expenses.csv')
    print(f"CSV file exported to:\n{file_path}")

#-----------------------------------------------------------------------
#   function to write to expenses json
#-----------------------------------------------------------------------
def write_json():
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file, indent=4)
        # note expenses is just variable name not specific. text is used often

#-----------------------------------------------------------------------
#   function to write to budgets json
#-----------------------------------------------------------------------
def write_budget_json():
    with open('budgets.json', 'w') as file:
        json.dump(budgets, file, indent=4)

#-----------------------------------------------------------------------
#   function to write to savings json
#-----------------------------------------------------------------------
def write_savings_json():
    with open('saving_goals.json', 'w') as file:
        json.dump(saving_goals, file, indent=4)       

#-----------------------------------------------------------------------
#   # while loop to get user input
#-----------------------------------------------------------------------

while True:
    show_menu()
    option = input("\nSelect Option: ")    
    if option == '1':
        add_expense()
        write_json()       
    elif option == '2':
        view_expenses()
    elif option == '3':
        print("Total Expenses Amount")
        total_expenses = add_up_expenses()
        print("${:.2f}".format(total_expenses))         
    elif option == '4':        
        view_categories()  
    elif option == '5':
        search_expenses() 
    elif option == '6':
        view_recent()  
    elif option == '7':
        delete_expense()                
    elif option == '8':
        set_category_budget()
    elif option == '9':        
        budget_stats = view_category_budget()
        print(tabulate(budget_stats,headers = "keys", tablefmt="fancy_grid"))        
        write_budget_json()
    elif option == '10':
        set_saving_goals()
    elif option == '11':
        monthly_report()
    elif option == '12':
        run_spending_trend()
    elif option == '13':
        csv_export()   
    elif option == '0':        
        write_json()
        write_budget_json()     
        print("Goodbye.")
        break
    else:
        print("Invalid action. Please try again.")

