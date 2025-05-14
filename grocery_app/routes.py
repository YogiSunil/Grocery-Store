
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
from grocery_app.extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        
        if existing_user:
            print(f"Signup failed: Username '{form.username.data}' already exists")
            flash('Username already exists. Please choose a different one.')
            return render_template('signup.html', form=form)
        elif existing_email:
            print(f"Signup failed: Email '{form.email.data}' already registered")
            flash('Email already registered. Please use a different email.')
            return render_template('signup.html', form=form)
            
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        print(f"New user created: {user.username} (ID: {user.id})")
        flash('Account created successfully! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            print(f"Login failed: User '{form.username.data}' not found")
            flash('Invalid username or password. Please try again.')
            return render_template('login.html', form=form)
            
        if not bcrypt.check_password_hash(user.password, form.password.data):
            print(f"Login failed: Invalid password for user '{form.username.data}'")
            flash('Invalid username or password. Please try again.')
            return render_template('login.html', form=form)
            
        login_user(user, remember=True)
        print(f"User '{user.username}' logged in successfully")
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.home'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/")
def home():


@main.route("/new_store", methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,

            address=form.address.data,
            created_by=current_user

        )
        db.session.add(new_store)
        db.session.commit()
        flash('New store was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_store.id))
    return render_template('new_store.html', form=form)

@main.route("/new_item", methods=['GET', 'POST'])
@login_required

def new_item():
    form = GroceryItemForm()
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,

            store=form.store.data,
            created_by=current_user

        )
        db.session.add(new_item)
        db.session.commit()
        flash('New item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):

    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.add(store)
        db.session.commit()
        flash('Store was updated successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))
    return render_template('store_detail.html', store=store, form=form)


@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):

    item = GroceryItem.query.get(item_id)

    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data

        db.session.add(item)
        db.session.commit()
        flash('Item was updated successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.append(item)
    db.session.commit()
    flash('Item added to shopping list!')
    return redirect(url_for('main.item_detail', item_id=item_id))

@main.route('/shopping_list')
@login_required
def shopping_list():
    shopping_list_items = current_user.shopping_list_items
    return render_template('shopping_list.html', shopping_list_items=shopping_list_items)

@main.route('/remove_from_shopping_list/<item_id>', methods=['POST'])
@login_required
def remove_from_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    if item in current_user.shopping_list_items:
        current_user.shopping_list_items.remove(item)
        db.session.commit()
        flash('Item removed from shopping list!')
    return redirect(url_for('main.shopping_list'))

