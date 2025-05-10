
# Grocery Store Tracker

A Flask web application for tracking grocery items across multiple stores and managing store inventories.

## Features

- Create and manage grocery stores with addresses
- Add and update grocery items with details like:
  - Name
  - Price
  - Category (Produce, Deli, Bakery, etc.)
  - Photo URL
- Associate items with specific stores
- View all stores and their inventory
- Add existing items to different stores
- Responsive UI with clean design
- Form validation for data integrity

## Technologies Used

- Flask
- SQLAlchemy
- WTForms
- SQLite Database
- HTML/CSS
- Python

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/YogiSunil/Grocery-Store.git
cd Grocery-Store
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Start the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Create a new store using the "New Store" button
2. Add items to the store using "New Item" button
3. View store details by clicking on store names
4. Edit store/item details on their respective detail pages
5. Add existing items to stores from the store detail page

## Project Structure

```
grocery_app/
├── static/          # Static files (CSS, images)
├── templates/       # HTML templates
├── forms.py         # Form classes
├── models.py        # Database models
├── routes.py        # Application routes
└── utils.py         # Utility functions
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.