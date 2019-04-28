from flask import render_template, redirect, request, session, flash
from config import db, datetime
from models import *
from customer_model import Customer, Address, State

### Customer controllers
## render index page with login and registration forms
def index():
    return render_template('index.html')

def show_registration():
    return render_template('register.html')

def do_registration():
    #validate new user data, create new user, redirect to ordering page
    print (request.form)
    errors=Customer.validate_info(request.form)
    print(errors)
    for error in errors:
        flash(error)
    if len(errors)==0:
        customer=Customer.new(request.form)
        session['MyWebsite_user_id']=customer.id
        session['name']=customer.name
        session['login_session']=Customer.get_session_key(customer.id)
        return redirect ('/quick')
    return redirect ('/user/register')

def show_login():
    return render_template('login.html')

def do_login():
    #validate login credentials, redirect to ordering page
    customer=Customer.validate_login(request.form)
    if customer:
        session['MyWebsite_user_id']=customer.id
        session['name']=customer.name
        session['login_session']=Customer.get_session_key(customer.id)
        return redirect('/quick')
    flash('Email or Password is incorrect.')
    return redirect('/user/login')

## render quick order page
def quick():
    return render_template('quick.html')

def show_custompizza():
    # customer_id=session['MyWebsite_user_id']
    # customer=Customer.get(customer_id)
    # orders=customer.orders
    orders=None
    sizes=Size.get_all()
    print(sizes)
    styles=Style.get_all()
    toppings_menu=ToppingMenu.get_all()
    return render_template('custompizza.html',sizes=sizes,styles=styles,toppings_menu=toppings_menu,orders=orders)

## customer nav partial
def nav():
    return render_template('nav.html')

def logout():
    session.clear()
    return redirect('/')
