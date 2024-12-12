from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse,HttpResponseForbidden
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Account,Transaction



def new_account(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        account_type = request.POST.get('account_type')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('account') 

        
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('account')

        account = Account.objects.create_user(
            email=email, 
            full_name=full_name, 
            phone=phone, 
            password=password
        )

        login(request, account)
        
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard') 

    return render(request, 'account.html') 

def home(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)  
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        user_account = request.user
        user_account.refresh_from_db()  
        user_name = user_account.full_name
        balance = user_account.balance
        
    else:
        user_name = "Guest"
        balance = 0.00

    return render(request, 'dashboard.html', {"user_name": user_name, "balance": balance})
    



def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount or Decimal(amount) <= 0:
            messages.error(request, 'Invalid deposit amount')
            return redirect('dashboard')
        
       
        user_account = request.user

        # Update the balance
        user_account.balance += Decimal(amount)
        user_account.save()

        # Create a deposit transaction record
        Transaction.objects.create(account=user_account, transaction_type=Transaction.DEPOSIT, amount=Decimal(amount))

        messages.success(request, f'Deposited ${amount} successfully!')
        

        return redirect('dashboard')
    return render(request, 'deposit.html')
def withdraw(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        # Check if the amount is valid 
        if not amount or Decimal(amount) <= 0:
            messages.error(request, 'Invalid withdrawal amount')
            return redirect('withdraw')  
        
        
        user_account = request.user

        
        if user_account.balance < Decimal(amount):
            messages.error(request, f'Insufficient balance -- your balance is ${user_account.balance}')
            return redirect('withdraw')  
        
        # Update the balance
        user_account.balance -= Decimal(amount)
        user_account.save()

        # Create a withdrawal transaction record
        Transaction.objects.create(account=user_account, transaction_type=Transaction.WITHDRAWAL, amount=Decimal(amount))

        messages.success(request, f'Withdrawn ${amount} successfully!')
        return redirect('dashboard')  # Redirect to the dashboard after a successful withdrawal
    return render(request, 'withdraw.html')
