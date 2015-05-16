from sqlalchemy.orm import aliased
from sqlalchemy import or_, and_
from application.lib.models import Message, MessageType, DirectMessage, SubjectMessage, GroupMessage, MessageBody, \
    Subject
from application.lib.validators import StringValidator, IntegerValidator, ChoicesValidator, DateValidator
from application.services.base import BasePersistanceService, BaseService
from application.lib.entities import PaginatedMessagesEntity
from application.services.group import GetUserGroups
from application.services.subject import GetUserSubjects
from application.services.user import GetUserConversators
from common.helper import Helper
from common import constants
from config import config


class PaginatedMessagesService(BasePersistanceService):

    message_class = None

    def input(self):
        return{
            'sender_id': IntegerValidator({'required': False, 'default': 0}),
            'items': IntegerValidator({'required': False, 'default': config.ITEMS_PER_PAGE}),
            'message_id': IntegerValidator({'required': False}),
            'order': ChoicesValidator({
                'required': False,
                'choices': constants.ORDER_CHOICES,
                'default': constants.ORDER_DESC
            }),
            'direction': ChoicesValidator({
                'required': False,
                'choices': constants.MESSAGES_PAGINATION_CHOICES,
                'default': constants.MESSAGES_PAGINATION_NEXT
            })
        }

    def output(self):
        return lambda x: Helper.instance_of(x, PaginatedMessagesEntity)

    def execute(self, args):

        message_class = self.message_class

        type_condition = {
            SubjectMessage: SubjectMessage.subject_id,
            GroupMessage: GroupMessage.group_id,
            DirectMessage: DirectMessage.user_id
        }

        orders = {
            constants.ORDER_ASC: message_class.created_at.asc(),
            constants.ORDER_DESC: message_class.created_at.desc()
        }

        filter_value = args.get('filter_value')
        items = args.get('items')
        message_id = args.get('message_id')
        order = args.get('order')
        direction = args.get('direction')
        sender_id = args.get('sender_id')
        more = False

        filter_field = type_condition.get(message_class)

        messages_query = self.session.query(message_class)
        check_more_messages_query = self.session.query(message_class)

        if message_class == DirectMessage:

            messages_query = messages_query.filter(or_(
                and_(DirectMessage.sender_id == sender_id, DirectMessage.user_id == filter_value),
                and_(DirectMessage.sender_id == filter_value, DirectMessage.user_id == sender_id)))

            check_more_messages_query = messages_query.filter(or_(
                and_(DirectMessage.sender_id == sender_id, DirectMessage.user_id == filter_value),
                and_(DirectMessage.sender_id == filter_value, DirectMessage.user_id == sender_id)))

        else:
            messages_query = messages_query.filter(filter_field == filter_value)
            check_more_messages_query = check_more_messages_query.filter(filter_field == filter_value)

        total = messages_query.count()

        if message_id:

            if direction == constants.MESSAGES_PAGINATION_PREVIOUS:
                messages_query = messages_query.\
                    filter(message_class.id < message_id).\
                    order_by(message_class.id.desc())

            elif direction == constants.MESSAGES_PAGINATION_NEXT:
                messages_query = messages_query.\
                    filter(message_class.id > message_id).\
                    order_by(message_class.id.asc())

        else:
            messages_query = messages_query.order_by(message_class.id.desc())

        messages_query = messages_query.limit(items)

        count = messages_query.count()

        messages_alias = aliased(message_class, messages_query.subquery('message'))

        order_clause = orders.get(order)
        aliased_messages_query = self.session.query(messages_alias).order_by(order_clause)
        messages = aliased_messages_query.all()

        if direction == constants.MESSAGES_PAGINATION_PREVIOUS:
            if order == constants.ORDER_ASC:
                last_message_idx = 0
            elif order == constants.ORDER_DESC:
                last_message_idx = -1
        elif direction == constants.MESSAGES_PAGINATION_NEXT:
            if order == constants.ORDER_ASC:
                last_message_idx = -1
            elif order == constants.ORDER_DESC:
                last_message_idx = 0

        if messages:
            last_message_id = messages[last_message_idx].id
            if message_id:
                if direction == constants.MESSAGES_PAGINATION_PREVIOUS:
                    more = check_more_messages_query.filter(message_class.id < last_message_id).count() > 0
                elif direction == constants.MESSAGES_PAGINATION_NEXT:
                    more = check_more_messages_query.filter(message_class.id > last_message_id).count() > 0

        return PaginatedMessagesEntity(messages, total, count, more)


class GetMessage(BasePersistanceService):
    def input(self):
        return {
            'message_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Message) or x is None

    def execute(self, args):
        message_id = args.get('message_id')

        message_query = self.session.query(Message)

        if message_query.filter(Message.id == message_id).count():
            message = message_query.get(message_id)
        else:
            message = None

        return message


class CheckMessageExists(BasePersistanceService):

    def input(self):
        return {
            'message_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):
        message_id = args.get('message_id')
        message_query = self.session.query(Message).\
            filter(Message.id == message_id)

        return message_query.count() == 1


class PutMessageBody(BasePersistanceService):
    def input(self):
        return {
            'body': StringValidator({'required': True, 'max_length': MessageBody.MAX_LENGTH}),
        }

    def output(self):
        return lambda x: Helper.instance_of(x, MessageBody)

    def execute(self, args):
        body = args.get('body')
        message_body = MessageBody(content=body)

        self.session.expunge_all()
        self.session.add(message_body)
        self.session.commit()
        return message_body


class PutMessage(BasePersistanceService):

    def input(self):
        return {
            'sender_id': IntegerValidator({'required': True}),
            'body': StringValidator({'required': True, 'max_length': MessageBody.MAX_LENGTH}),
            'type': ChoicesValidator({'required': True, 'choices': MessageType.CHOICES}),
            'created_at': DateValidator({'required': True}),
            'recipient_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Message)

    @staticmethod
    def get_message_class(message_type):
        dispatcher = {
            MessageType.DIRECT_MESSAGE: DirectMessage,
            MessageType.GROUP_MESSAGE: GroupMessage,
            MessageType.SUBJECT_MESSAGE: SubjectMessage
        }

        return dispatcher.get(message_type)

    @staticmethod
    def adapt_args(args):
        recipient_id = args.get('recipient_id')
        message_type = args.get('type')

        dispatcher = {
            MessageType.DIRECT_MESSAGE: 'user_id',
            MessageType.GROUP_MESSAGE: 'group_id',
            MessageType.SUBJECT_MESSAGE: 'subject_id'
        }

        new_key = dispatcher.get(message_type)
        args[new_key] = recipient_id
        args.pop('recipient_id')

    def execute(self, args):
        message_type = args.get('type')
        body = args.pop('body')

        put_message_body_srv = PutMessageBody()
        message_body = put_message_body_srv.call({'body': body})

        message_cls = self.get_message_class(message_type)
        self.adapt_args(args)

        args['body_id'] = message_body.id
        message = message_cls(**args)

        self.session.expunge_all()
        self.session.merge(message_body)
        self.session.add(message)
        self.session.commit()
        return message


class PutMessageInputAndOutputContractMixin(BaseService):
    def input(self):
        return {
            'sender_id': IntegerValidator({'required': True}),
            'body': StringValidator({'required': True, 'max_length': MessageBody.MAX_LENGTH}),
            'created_at': DateValidator({'required': True}),
            'recipient_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Message)

    def execute(self, args):
        raise NotImplementedError()


class PutSubjectMessage(PutMessageInputAndOutputContractMixin, BaseService):
    def execute(self, args):
        args.update({'type': MessageType.SUBJECT_MESSAGE})
        put_message_srv = PutMessage()
        return put_message_srv.call(args)


class PutGroupMessage(PutMessageInputAndOutputContractMixin, BaseService):
    def execute(self, args):
        args.update({'type': MessageType.GROUP_MESSAGE})
        put_message_srv = PutMessage()
        return put_message_srv.call(args)


class PutDirectMessage(PutMessageInputAndOutputContractMixin, BaseService):

    def execute(self, args):
        args.update({'type': MessageType.DIRECT_MESSAGE})
        put_message_srv = PutMessage()
        return put_message_srv.call(args)


class GetSubjectMessages(PaginatedMessagesService):

    message_class = SubjectMessage

    def input(self):
        super_input = super(GetSubjectMessages, self).input()
        super_input.update({'subject_id': IntegerValidator({'required': True})})
        return super_input

    def execute(self, args):
        subject_id = args.pop('subject_id')
        args['filter_value'] = subject_id
        return super(GetSubjectMessages, self).execute(args)


class GetGroupMessages(PaginatedMessagesService):

    message_class = GroupMessage

    def input(self):
        super_input = super(GetGroupMessages, self).input()
        super_input.update({'group_id': IntegerValidator({'required': True})})
        return super_input

    def execute(self, args):
        group_id = args.pop('group_id')
        args['filter_value'] = group_id
        return super(GetGroupMessages, self).execute(args)


class GetDirectMessages(PaginatedMessagesService):

    message_class = DirectMessage

    def input(self):
        super_input = super(GetDirectMessages, self).input()
        super_input.update({'sender_id': IntegerValidator({'required': True})})
        super_input.update({'recipient_id': IntegerValidator({'required': True})})
        return super_input

    def execute(self, args):
        recipient_id = args.pop('recipient_id')
        args['filter_value'] = recipient_id
        return super(GetDirectMessages, self).execute(args)


class GetLastMessage(BasePersistanceService):

    message_cls = None

    def input(self):
        return {
            'filter_value': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, self.message_cls) or x is None

    def execute(self, args):

        filter_value = args.get('filter_value')

        message_cls = self.message_cls

        filter_mapping = {
            SubjectMessage: SubjectMessage.subject_id,
            GroupMessage: GroupMessage.group_id,
            DirectMessage: DirectMessage.user_id
        }

        filter_field = filter_mapping.get(message_cls)

        last_message_query = self.session.query(message_cls).\
            filter(filter_field == filter_value).\
            order_by(message_cls.created_at.desc()).\
            limit(1)

        if last_message_query.count():
            message = last_message_query.all()[0]
        else:
            message = None

        return message


class GetLastSubjectMessage(GetLastMessage):

    message_cls = SubjectMessage

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, SubjectMessage) or x is None

    def execute(self, args):
        args['filter_value'] = args.pop('subject_id', None)
        return super(GetLastSubjectMessage, self).execute(args)


class GetLastGroupMessage(GetLastMessage):

    message_cls = GroupMessage

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, GroupMessage) or x is None

    def execute(self, args):
        args['filter_value'] = args.pop('group_id', None)
        return super(GetLastGroupMessage, self).execute(args)


class GetLastConversationMessage(BasePersistanceService):

    def input(self):
        return {
            'my_id': IntegerValidator({'required': True}),
            'its_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, DirectMessage) or x is None

    def execute(self, args):

        my_id = args.get('my_id')
        its_id = args.get('its_id')

        message_query = self.session.query(DirectMessage).\
            filter(or_(
                and_(DirectMessage.sender_id == my_id, DirectMessage.user_id == its_id),
                and_(DirectMessage.sender_id == its_id, DirectMessage.user_id == my_id))).\
            order_by(DirectMessage.created_at.desc()).limit(1)

        if message_query.count():
            message = message_query.all()[0]
        else:
            message = None
        return message


class GetUserSubjectsLastMessages(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, SubjectMessage) or x == []

    def execute(self, args):

        get_last_subject_message_srv = GetLastSubjectMessage()

        def get_last_subject_message(subject):
            last_message = get_last_subject_message_srv.call({
                'subject_id': subject.id
            })
            return last_message

        user_id = args.get('user_id')

        get_user_subjects_srv = GetUserSubjects()
        subjects = get_user_subjects_srv.call({
            'user_id': user_id
        })

        return filter(bool, map(get_last_subject_message, subjects))


class GetUserGroupsLastMessages(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, GroupMessage) or x == []

    def execute(self, args):
        get_last_group_message_srv = GetLastGroupMessage()

        def get_last_group_message(group):
            last_message = get_last_group_message_srv.call({
                'group_id': group.id
            })
            return last_message

        user_id = args.get('user_id')

        get_user_groups_srv = GetUserGroups()
        groups = get_user_groups_srv.call({
            'user_id': user_id
        })

        return filter(bool, map(get_last_group_message, groups))


class GetUserConversationsLastMessages(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, DirectMessage) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        get_conversation_last_message_srv = GetLastConversationMessage()

        def get_last_conversation_message(its):
            last_message = get_conversation_last_message_srv.call({
                'my_id': user_id,
                'its_id': its.id
            })

            return last_message

        get_user_conversators_srv = GetUserConversators()
        conversators = get_user_conversators_srv.call({
            'user_id': user_id
        })

        return filter(bool, map(get_last_conversation_message, conversators))