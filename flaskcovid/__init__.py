from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "ddd1281150ebdef99b70edda7b2d15ba"

from flaskcovid import routes
