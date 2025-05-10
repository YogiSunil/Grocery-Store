
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    form = GroceryStoreForm()
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data
        )
        db.session.add(new_store)
        db.session.commit()
        flash('New store was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_store.id))
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = GroceryItemForm()
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash('New item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get_or_404(store_id)
    form = GroceryStoreForm(obj=store)
    all_items = GroceryItem.query.all()
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()
        flash('Store was updated successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))
    return render_template('store_detail.html', store=store, form=form, all_items=all_items)

@main.route('/store/<store_id>/add_item/<item_id>', methods=['POST'])
def add_item_to_store(store_id, item_id):
    store = GroceryStore.query.get_or_404(store_id)
    item = GroceryItem.query.get_or_404(item_id)
    item.store = store
    db.session.commit()
    flash('Item added to store successfully.')
    return redirect(url_for('main.store_detail', store_id=store_id))

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.commit()
        flash('Item was updated successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    return render_template('item_detail.html', item=item, form=form)
