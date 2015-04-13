
class PaginatedEntity(object):

    objects = []
    total = 0
    count = 0

    def __init__(self, objects=[], total=0, count=0):
        if objects:
            self.objects = objects

        if total:
            self.total = total

        if count:
            self.count = count

    def to_dict(self):
        return {
            'total': self.total,
            'count': self.count,
            'objects': self.objects
        }


class PaginatedMessagesEntity(PaginatedEntity):

    last_id = 0
    order = None

    def __init__(self, objects=[], total=0, count=0, last_id=0, order=None):
        super(PaginatedMessagesEntity, self).__init__(objects, total, count)

        if last_id:
            self.last_id = last_id

        if order:
            self.order = order

    def to_dict(self):
        super_dict = super(PaginatedMessagesEntity, self).to_dict()
        messages = super_dict.pop('objects', [])
        super_dict.update({
            'last_id': self.last_id,
            'order': self.order,
            'messages': messages
        })

        return super_dict












