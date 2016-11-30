# for local testing
from app import app, db
from app.views import views

db.create_all()

app.register_blueprint(views)

# go to localhost:8000 to view
app.run(host="0.0.0.0", port=8000)
