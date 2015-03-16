from flask import Flask

from views import SubjectsView
# from views import GroupsView, SubjectMessagesView

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.add_url_rule('/subjects/', view_func=SubjectsView.as_view('subjects'))
# app.add_url_rule('/groups/', view_func=GroupsView.as_view('groups'))
# app.add_url_rule('/subjects/<int:subject_id>/messages/', view_func=SubjectMessagesView.as_view('subject_messages'))