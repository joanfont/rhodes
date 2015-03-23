from flask import Flask

from views import SubjectsView, SubjectDetailView, SubjectMessagesView, SubjectGroupsView, GroupDetailView, \
    GroupMessagesView, ProfileView, SubjectTeachersView, SubjectStudentsView

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.add_url_rule('/user/', view_func=ProfileView.as_view('profile'))

app.add_url_rule('/user/subjects/', view_func=SubjectsView.as_view('subjects'))
app.add_url_rule('/user/subjects/<subject_id>/', view_func=SubjectDetailView.as_view('subject'))
app.add_url_rule('/user/subjects/<subject_id>/messages/', view_func=SubjectMessagesView.as_view('subject_messages'),
                 methods=['GET', 'POST'])
app.add_url_rule('/user/subjects/<subject_id>/teachers/', view_func=SubjectTeachersView.as_view('subject_teachers'))
app.add_url_rule('/user/subjects/<subject_id>/students/', view_func=SubjectStudentsView.as_view('subject_students'))

app.add_url_rule('/user/subjects/<subject_id>/groups/', view_func=SubjectGroupsView.as_view('subject_groups'))
app.add_url_rule('/user/subjects/<subject_id>/groups/<group_id>/', view_func=GroupDetailView.as_view('subject_group'))
app.add_url_rule('/user/subjects/<subject_id>/groups/<group_id>/messages/',
                 view_func=GroupMessagesView.as_view('subject_group_messages'), methods=['GET', 'POST'])
