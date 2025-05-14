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
    all_stores = GroceryStore.query.all()
    return render_template("home.html", all_stores=all_stores)

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
    current_user.shopping_list_items.remove(item)
    db.session.commit()
    flash('Item removed from shopping list!')
    return redirect(url_for('main.shopping_list'))

@main.route('/delete_store/<store_id>', methods=['POST'])
@login_required
def delete_store(store_id):
    store = GroceryStore.query.get(store_id)
    db.session.delete(store)
    db.session.commit()
    flash('Store deleted successfully.')
    return redirect(url_for('main.home'))
@main.route('/delete_item/<item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = GroceryItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.')
    return redirect(url_for('main.store_detail', store_id=item.store.id))
@main.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted successfully.')
    return redirect(url_for('main.home'))
@main.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = SignUpForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('main.profile', username=current_user.username))
    return render_template('update_profile.html', form=form)
@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)   
@main.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    if query:
        items = GroceryItem.query.filter(GroceryItem.name.ilike(f'%{query}%')).all()
    else:
        items = []
    return render_template('search_results.html', items=items, query=query)
@main.route('/store/<store_id>/items')
@login_required
def store_items(store_id):
    store = GroceryStore.query.get(store_id)
    items = store.items
    return render_template('store_items.html', store=store, items=items)
@main.route('/store/<store_id>/items/<item_id>')
@login_required

def store_item_detail(store_id, item_id):
    store = GroceryStore.query.get(store_id)
    item = GroceryItem.query.get(item_id)
    return render_template('store_item_detail.html', store=store, item=item)

@main.route('/store/<store_id>/items/<item_id>/add_to_shopping_list', methods=['POST'])
@login_required
def add_store_item_to_shopping_list(store_id, item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.append(item)
    db.session.commit()
    flash('Item added to shopping list!')
    return redirect(url_for('main.store_item_detail', store_id=store_id, item_id=item_id))

@main.route('/store/<store_id>/items/<item_id>/remove_from_shopping_list', methods=['POST'])
@login_required
def remove_store_item_from_shopping_list(store_id, item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.remove(item)
    db.session.commit()
    flash('Item removed from shopping list!')
    return redirect(url_for('main.store_item_detail', store_id=store_id, item_id=item_id))

@main.route('/store/<store_id>/items/<item_id>/delete', methods=['POST'])
@login_required
def delete_store_item(store_id, item_id):
    item = GroceryItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.')
    return redirect(url_for('main.store_items', store_id=store_id))

@main.route('/store/<store_id>/items/<item_id>/update', methods=['GET', 'POST'])
@login_required
def update_store_item(store_id, item_id):
    store = GroceryStore.query.get_or_404(store_id)  # Query the store using store_id
    item = GroceryItem.query.get_or_404(item_id)
    form = GroceryItemForm(obj=item)

    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.commit()
        flash('Item updated successfully.')
        return redirect(url_for('main.store_item_detail', store_id=store_id, item_id=item.id))

    return render_template('update_store_item.html', form=form, store=store, item=item)

@main.route('/store/<store_id>/items/<item_id>/add_to_favorites', methods=['POST'])
@login_required
def add_store_item_to_favorites(store_id, item_id):
    item = GroceryItem.query.get(item_id)
    current_user.favorite_items.append(item)
    db.session.commit()
    flash('Item added to favorites!')
    return redirect(url_for('main.store_item_detail', store_id=store_id, item_id=item_id))
@main.route('/store/<store_id>/items/<item_id>/remove_from_favorites', methods=['POST'])
@login_required
def remove_store_item_from_favorites(store_id, item_id):
    item = GroceryItem.query.get(item_id)
    current_user.favorite_items.remove(item)
    db.session.commit()
    flash('Item removed from favorites!')
    return redirect(url_for('main.store_item_detail', store_id=store_id, item_id=item_id))

@main.route('/store/<store_id>/items/<item_id>/favorite', methods=['POST'])
@login_required
def favorite_store_item(store_id, item_id):
    item = GroceryItem.query.get(item_id)
    if item in current_user.favorite_items:
        current_user.favorite_items.remove(item)
        flash('Item removed from favorites!')
    else:
        current_user.favorite_items.append(item)
        flash('Item added to favorites!')
    db.session.commit()
    return redirect(url_for('main.store_item_detail', store_id=store_id, item_id=item_id))

@main.route('/store/<store_id>/items/<item_id>/unfavorite', methods=['POST'])
@login_required
def unfavorite_store_item(store_id, item_id):
    item = GroceryItem.query.get(item_id)
    if item in current_user.favorite_items:
        current_user.favorite_items.remove(item)
        flash('Item removed from favorites!')
    else:
        flash('Item not in favorites!')
    db.session.commit()
    return redirect(url_for('main.store_item_detail', store_id=store_id, item_id=item_id))

@main.route('/iteam_list')
@login_required
def iteam_list():
    all_items = GroceryItem.query.all()
    all_stores = GroceryStore.query.all()
    return render_template('iteam_list.html', all_items=all_items, all_stores=all_stores)

@main.route('/add_item_to_store/<item_id>', methods=['POST'])
@login_required
def add_item_to_store(item_id):
    store_id = request.form.get('store_id')
    store = GroceryStore.query.get(store_id)
    item = GroceryItem.query.get(item_id)
    if store and item:
        if item not in store.items:
            store.items.append(item)
            db.session.commit()
            flash(f"{item.name} added to {store.title}!")
        else:
            flash(f"{item.name} is already in {store.title}.")
    else:
        flash("Invalid store or item.")
    return redirect(url_for('main.iteam_list'))