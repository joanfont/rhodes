from api.views import subject as subject_views
from api.views import group as group_views
from api.views import message as message_views
from api.views import user as user_views
from api.views import conversation as conversation_views
from api.views import misc as misc_views


routing = {
    '/config/': {
        'class': misc_views.ConfigView,
        'name': 'config',
        'methods': ['GET']
    },
    '/login/': {
        'class': user_views.LoginView,
        'name': 'login',
        'methods': ['GET']
    },
    '/user/': {
        'class': user_views.ProfileView,
        'name': 'profile',
        'methods': ['GET']
    },
    '/user/subjects/': {
        'class': subject_views.SubjectsView,
        'name': 'user_subjects',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/': {
        'class': subject_views.SubjectDetailView,
        'name': 'user_subject',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/messages/': [
        {
            'class': message_views.ListSubjectMessagesView,
            'name': 'user_subject_messages',
            'methods': ['GET']
        },
        {
            'class': message_views.PostSubjectMessageView,
            'name': 'user_subject_messages_post',
            'methods': ['POST']
        }
    ],
    '/user/subjects/<subject_id>/messages/<message_id>/': {
        'class': message_views.SubjectMessageDetailView,
        'name': 'user_subject_message',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/messages/<message_id>/<direction>/': {
        'class': message_views.ListPaginatedSubjectMessagesView,
        'name': 'user_subject_messages_paginated',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/teachers/': {
        'class': user_views.SubjectTeachersView,
        'name': 'user_subject_teachers',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/students/': {
        'class': user_views.SubjectStudentsView,
        'name': 'user_subject_students',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/groups/': {
        'class': group_views.SubjectGroupsView,
        'name': 'user_subject_groups',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/groups/<group_id>/': {
        'class': group_views.GroupDetailView,
        'name': 'user_subject_group',
        'methods': ['GET'],
    },
    '/user/subjects/<subject_id>/groups/<group_id>/messages/': [
        {
            'class': message_views.ListGroupMessagesView,
            'name': 'user_subject_group_messages',
            'methods': ['GET']
        },
        {
            'class': message_views.PostGroupMessageView,
            'name': 'user_group_messages_post',
            'methods': ['POST']
        }
    ],
    '/user/subjects/<subject_id>/groups/<group_id>/messages/<message_id>/': {
        'class': message_views.GroupMessageDetailView,
        'name': 'user_subject_group_message',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/groups/<group_id>/messages/<message_id>/<direction>/': {
        'class': message_views.ListPaginatedGroupMessagesView,
        'name': 'user_subject_group_messages_paginated',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/groups/<group_id>/students/': {
        'class': user_views.GroupStudentsView,
        'name': 'user_subject_group_students',
        'methods': ['GET']
    },
    '/user/teachers/': {
        'class': user_views.TeacherPeersView,
        'name':  'user_teacher_peers',
        'methods': ['GET']
    },
    '/user/teachers/<peer_id>/': {
        'class': user_views.TeacherDetailPeerView,
        'name':  'user_teachers_peer_detail',
        'methods': ['GET']
    },
    '/user/students/': {
        'class': user_views.StudentPeersView,
        'name':  'user_teacher_student_peers',
        'methods': ['GET']
    },
    '/user/students/<peer_id>/': {
        'class': user_views.StudentDetailPeerView,
        'name':  'user_students_peer_detail',
        'methods': ['GET']
    },
    '/user/chats/': {
        'class': conversation_views.ListConversationsView,
        'name': 'user_chats',
        'methods': ['GET']
    },
    '/user/chats/<peer_id>/': {
        'class': conversation_views.ConversationDetailView,
        'name': 'user_chat',
        'methods': ['GET']
    },
    '/user/chats/<peer_id>/messages/': [
        {
            'class': message_views.ListDirectMessagesView,
            'name': 'user_chat_messages',
            'methods': ['GET']
        },
        {
            'class': message_views.PostDirectMessageView,
            'name': 'user_chat_message_post',
            'methods': ['POST']
        }
    ],
    '/user/chats/<peer_id>/messages/<message_id>/<direction>/': {
        'class': message_views.ListPaginatedDirectMessagesView,
        'name': 'user_chat_paginated_messages',
        'methods': ['GET']
    }
}