from flask import Flask

from views import SubjectsView, SubjectDetailView, SubjectMessagesView

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.add_url_rule('/subjects/', view_func=SubjectsView.as_view('subjects'))

app.add_url_rule('/subjects/<int:subject_id>/', view_func=SubjectDetailView.as_view('subject'))
app.add_url_rule('/subjects/<int:subject_id>/messages/', view_func=SubjectMessagesView.as_view('subject_messages'),
                 methods=['GET', 'POST'])