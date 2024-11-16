from flask import Flask
from app.routes import recommend

app = Flask(__name__)

# Register routes
app.register_blueprint(recommend)

if __name__ == "__main__":
    app.run(debug=True)
