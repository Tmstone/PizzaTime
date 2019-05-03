from flask import render_template, redirect, request, session, flash
from config import db, datetime #, stripe_keys
from models import *
from customer_model import Customer, Address, State

# Stripe API #
# https://stripe.com/docs/testing
# https://testdriven.io/blog/adding-a-custom-stripe-checkout-to-a-flask-app/
# Visa card test number: 4242424242424242
import stripe


def show_checkout():
    #print(stripe_keys['publishable_key'])
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    order=Order.get_entering(customer.id)
    return render_template('checkout.html',
    order=order,key=stripe_keys['publishable_key'])

def charge():
    # Action route handler from Stripe
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    order=Order.get_entering(customer.id)
    # Stripe token
    stripe_customer = stripe.Customer.create(
        email=customer.email,
        source=request.form['stripeToken']
    )
    # amount in cents, must be type int
    amount=int(order.total()*100)
    # Process charge with stripe token
    stripe.Charge.create(
        customer=stripe_customer.id,
        amount=amount,
        currency='usd',
        description='OrderID:'+str(order.id)
    )
    # change order status so it shows up in kitchen dashboard
    order.submit()
    # show a response to the user.
    return render_template('charge.html', amount=amount)

### Customer controllers
## render index page with login and registration forms
def index():
    return render_template('index.html')

def show_registration():
    return render_template('register.html')

def do_registration():
    #validate new user data, create new user, redirect to ordering page
    # print (request.form)
    errors=Customer.validate_info(request.form)
    print(errors)
    for error in errors:
        flash(error)
    if len(errors)==0:
        customer=Customer.new(request.form)
        session['MyWebsite_customer_id']=customer.id
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
        session['MyWebsite_customer_id']=customer.id
        session['name']=customer.name
        session['login_session']=Customer.get_session_key(customer.id)
        return redirect('/quick')
    flash('Email or Password is incorrect.')
    return redirect('/user/login')

## render quick order page
def quick():
    name = session['name']
    userid = session['MyWebsite_customer_id']
    print(name)
    return render_template('quick.html',
    name = name,
    userid = userid,
    )

def show_custompizza():
    # print('customer id',session['MyWebsite_customer_id'])
    customer_id=session['MyWebsite_customer_id']
    # print('customer id',customer_id)
    customer=Customer.get(customer_id)
    # print(customer)
    order=Order.get_entering(customer.id)
    if not order:
        order=Order.new(customer_id)
    print(order)
    sizes=Size.get_all()
    # print(sizes)
    styles=Style.get_all()
    order_types=OrderType.get_all()
    # print("order types:",order_types)
    toppings_menu=ToppingMenu.get_all()
    print(order.pizzas)
    return render_template('custompizza.html',sizes=sizes,styles=styles,toppings_menu=toppings_menu,order_types=order_types,order=order)
    # return render_template('custompizza.html')

## customer nav partial
def nav():
    cust_name = Customer.query.get(session['MyWebsite_customer_id'])
    name = cust_name.name
    return render_template('nav.html',
    name = name
    )

def add_pizza():
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    print("add pizza form:",request.form)
    order=Order.get_entering(customer.id)
    if not order:
        order=Order.new(customer_id)
    new_pizza=Pizza.new(order.id,request.form)
    return redirect('/create')

#render account page
def cust_account():
    customer_id=session['MyWebsite_customer_id']
    customer=Customer.get(customer_id)
    cust_address=Address.query.get(customer_id)
    #print('*'*90)
    #print(cust_address)
    #Get past orders
    order=Order.get_entering(customer.id)
    return render_template('account.html',
    customer = customer,
    order = order
    )
#
def cust_update():
    update = Customer.edit_user(request.form)
    return redirect('/account')

def logout():
    session.clear()
    return redirect('/')
