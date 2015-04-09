from api import app
from config import config


def setup_config(application):
    application.config['JSON_SORT_KEYS'] = False
    application.config['SQLALCHEMY_DATABASE_URI'] = config.DB_DSN

    return application


def setup_logging(application):

    from logging.handlers import RotatingFileHandler
    import logging

    formatter = logging.Formatter('[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(config.LOG_FILE, maxBytes=10000000, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    application.logger.addHandler(file_handler)

    return application


def setup_routing(application):

    from views import subject as subject_views
    from views import group as group_views
    from views import message as message_views
    from views import user as user_views

    application.add_url_rule('/login/', view_func=user_views.LoginView.as_view('login'))

    application.add_url_rule('/user/', view_func=user_views.ProfileView.as_view('profile'))

    application.add_url_rule('/user/subjects/', view_func=subject_views.SubjectsView.as_view('subjects'))
    application.add_url_rule('/user/subjects/<subject_id>/', view_func=subject_views.SubjectDetailView.as_view('subject'))
    application.add_url_rule('/user/subjects/<subject_id>/messages/',
                             view_func=message_views.SubjectMessagesView.as_view('subject_messages'),
                             methods=['GET', 'POST'])

    application.add_url_rule('/user/subjects/<subject_id>/teachers/',
                             view_func=user_views.SubjectTeachersView.as_view('subject_teachers'))
    application.add_url_rule('/user/subjects/<subject_id>/students/',
                             view_func=user_views.SubjectStudentsView.as_view('subject_students'))

    application.add_url_rule('/user/subjects/<subject_id>/groups/',
                             view_func=group_views.SubjectGroupsView.as_view('subject_groups'))
    application.add_url_rule('/user/subjects/<subject_id>/groups/<group_id>/',
                             view_func=group_views.GroupDetailView.as_view('subject_group'))
    application.add_url_rule('/user/subjects/<subject_id>/groups/<group_id>/messages/',
                             view_func=message_views.GroupMessagesView.as_view('subject_group_messages'),
                             methods=['GET', 'POST'])

    return application


def setup_error_handlers(application):

    return application


def configure(application):

    application = setup_config(application)
    application = setup_logging(application)
    application = setup_routing(application)
    application = setup_error_handlers(application)

    return application


app = configure(app)