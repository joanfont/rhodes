
class PaginatedEntity(object):

    objects = []
    total = 0
    count = 0

    def __init__(self, objects=[], total=0, count=0, **options):

        if objects:
            self.objects = map(lambda x: x.to_dict(**options), objects)

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

    more = True

    def __init__(self, objects=[], total=0, count=0, more=True, **options):
        super(PaginatedMessagesEntity, self).__init__(objects, total, count, **options)

        if more:
            self.more = more

    def to_dict(self):
        super_dict = super(PaginatedMessagesEntity, self).to_dict()
        messages = super_dict.pop('objects', [])
        super_dict.update({
            'more': self.more,
            'messages': messages
        })

        return super_dict












