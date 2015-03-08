from flask import Flask

from views import SubjectsView

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.add_url_rule('/subjects/', view_func=SubjectsView.as_view('subjects'))
