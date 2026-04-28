# for local testing
from app import app, db
from app.views import views

app.register_blueprint(views)

with app.app_context():
    db.create_all()

# go to localhost:8000 to view
app.run(host="0.0.0.0", port=8000)
