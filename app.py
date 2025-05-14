
from grocery_app.extensions import app, db
from grocery_app.routes import main, auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
