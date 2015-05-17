from api.views import subject as subject_views
from api.views import group as group_views
from api.views import message as message_views
from api.views import user as user_views
from api.views import misc as misc_views
from api.views import notification as notification_views

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
    '/user/': {
        'class': user_views.UpdateAvatarView,
        'name': 'user_update_avatar',
        'methods': ['PATCH']
    },
    '/user/avatar/': {
        'class': user_views.AvatarView,
        'name': 'user_view_avatar',
        'methods': ['GET']
    },
    '/user/subjects/': {
        'class': subject_views.ListSubjectsView,
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
        'class': user_views.ListSubjectTeachersView,
        'name': 'user_subject_teachers',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/students/': {
        'class': user_views.ListSubjectStudentsView,
        'name': 'user_subject_students',
        'methods': ['GET']
    },
    '/user/subjects/<subject_id>/groups/': {
        'class': group_views.ListSubjectGroupsView,
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
        'class': user_views.ListGroupStudentsView,
        'name': 'user_subject_group_students',
        'methods': ['GET']
    },
    '/user/teachers/': {
        'class': user_views.ListTeacherPeersView,
        'name':  'user_teacher_peers',
        'methods': ['GET']
    },
    '/user/teachers/<peer_id>/': {
        'class': user_views.TeacherDetailView,
        'name':  'user_teachers_peer_detail',
        'methods': ['GET']
    },
    '/user/teachers/<peer_id>/avatar/': {
        'class': user_views.TeacherAvatarView,
        'name': 'user_teacher_avatar',
        'methods': ['GET']
    },
    '/user/students/': {
        'class': user_views.ListStudentPeersView,
        'name':  'user_teacher_student_peers',
        'methods': ['GET']
    },
    '/user/students/<peer_id>/': {
        'class': user_views.StudentDetailView,
        'name':  'user_students_peer_detail',
        'methods': ['GET']
    },
    '/user/students/<peer_id>/avatar/': {
        'class': user_views.StudentAvatarView,
        'name': 'user_student_avatar',
        'methods': ['GET']
    },
    '/user/chats/': {
        'class': user_views.ListConversatorsView,
        'name': 'user_chats',
        'methods': ['GET']
    },
    '/user/chats/<peer_id>/': {
        'class': user_views.ConversatorDetailView,
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
    },
    '/user/notifications/': {
        'class': notification_views.MessagesNotificationsView,
        'name': 'user_notifications',
        'methods': ['GET']
    },
    '/user/notifications/subject/': {
        'class': notification_views.SubjectMessagesNotificationsView,
        'name': 'user_subject_notifications',
        'methods': ['GET']
    },
    '/user/notifications/group/': {
        'class': notification_views.GroupMessagesNotificationsView,
        'name': 'user_groups_notifications',
        'methods': ['GET']
    },
    '/user/notifications/chat/': {
        'class': notification_views.ConversationNotificationsView,
        'name': 'user_chats_notifications',
        'methods': ['GET']
    },

}