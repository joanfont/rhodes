from api import app

from views import subject as subject_views
from views import group as group_views
from views import message as message_views
from views import user as user_views

app.add_url_rule('/login/', view_func=user_views.LoginView.as_view('login'))

app.add_url_rule('/user/', view_func=user_views.ProfileView.as_view('profile'))

app.add_url_rule('/user/subjects/', view_func=subject_views.SubjectsView.as_view('subjects'))
app.add_url_rule('/user/subjects/<subject_id>/', view_func=subject_views.SubjectDetailView.as_view('subject'))
app.add_url_rule('/user/subjects/<subject_id>/messages/',
                 view_func=message_views.SubjectMessagesView.as_view('subject_messages'),
                 methods=['GET', 'POST'])

app.add_url_rule('/user/subjects/<subject_id>/teachers/',
                 view_func=user_views.SubjectTeachersView.as_view('subject_teachers'))
app.add_url_rule('/user/subjects/<subject_id>/students/',
                 view_func=user_views.SubjectStudentsView.as_view('subject_students'))

app.add_url_rule('/user/subjects/<subject_id>/groups/',
                 view_func=group_views.SubjectGroupsView.as_view('subject_groups'))
app.add_url_rule('/user/subjects/<subject_id>/groups/<group_id>/',
                 view_func=group_views.GroupDetailView.as_view('subject_group'))
app.add_url_rule('/user/subjects/<subject_id>/groups/<group_id>/messages/',
                 view_func=message_views.GroupMessagesView.as_view('subject_group_messages'), methods=['GET', 'POST'])
