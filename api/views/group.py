from api.lib.decorators import user_belongs_to_subject, group_exists, user_belongs_to_group, \
    group_belongs_to_subject, auth_token_required
from api.lib.decorators import subject_exists
from api.lib.mixins import ListAPIViewMixin, ModelResponseMixin
from application.services.group import GetGroup, GetSubjectUserGroups


class SubjectGroupsView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        subject_id = kwargs.get('subject_id')

        get_subject_user_groups_srv = GetSubjectUserGroups()
        groups = get_subject_user_groups_srv.call({'subject_id': subject_id, 'user_id': user.id})

        return groups


class GroupDetailView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @subject_exists
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    def get_action(self, *args, **kwargs):

        group_id = kwargs.get('group_id')

        get_group_srv = GetGroup()
        group = get_group_srv.call({'group_id': group_id})

        return group


