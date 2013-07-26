'''
Fieldset shall provide a interface that behaves like::

.. code-block:: python

    fieldsets = Fieldsets(
        Fieldset(
            'information',
            _('Information'),
            fields=(
                'title',
                'description',
                'links',
            ),
            classes=('wide',)),
        Fieldset(
            'images',
            'video',
            'attribution',
            id='media',
            name=_('Media'),
            classes=('wide',)),
    )

    fieldsets = fieldsets.move_fieldset('information', after='media')
    fieldsets = fieldsets.move_field('images', after='video')
    fieldsets = fieldsets.move_field('links', after='attribution')
    fieldsets = fieldsets.add_field('a_field_that_was_not_yet_listed_in_the_fieldset', before='attribution')
    fieldsets = fieldsets.remove_fieldset('media')
'''


class Fieldsets(object):
    def __init__(self, *fieldsets):
        self._fieldsets = []
        for fieldset in fieldsets:
            self.append(fieldset)

    def __eq__(self, other):
        return self._fieldsets == other._fieldsets

    def __nonzero__(self):
        return bool(self._fieldsets)

    def __contains__(self, field):
        '''
        Checks if the given field is contained in one of the fieldsets.
        '''
        for fieldset in self._fieldsets:
            if field in fieldset:
                return True
        return False

    def __len__(self):
        return len(self._fieldsets)

    def __getitem__(self, key):
        return self._fieldsets[key]

    def copy(self):
        return Fieldsets(*self._fieldsets)

    @property
    def fields(self):
        fields = []
        for fieldset in self._fieldsets:
            fields.extend(fieldset.fields)
        return fields

    def append(self, fieldset):
        self._fieldsets.append(fieldset)

    def remove_fieldset(self, id):
        if type(id) is int:
            new = self.copy()
            del new._fieldsets[id]
            return new
        else:
            for i, fieldset in enumerate(self._fieldsets):
                if fieldset.id == id:
                    new = self.copy()
                    del new._fieldsets[i]
                    return new
        raise ValueError('Fieldset with id "{}" does not exist.'.format(id))

class Fieldset(object):
    def __init__(self, *fields, **kwargs):
        self._fields = list(fields)
        self.id = kwargs.pop('id', None)
        self.name = kwargs.pop('name', None)

    def __eq__(self, other):
        return self._fields == other._fields

    def __nonzero__(self):
        return bool(self._fields)

    def __contains__(self, field):
        return field in self._fields

    def index(self, field):
        return self._fields.index(field)

    def copy(self):
        return Fieldset(*self._fields)

    @property
    def fields(self):
        return self._fields[:]

    def _determine_new_index(self, after=None, before=None):
        if before is None and after is None:
            raise ValueError(
                'Specify either `before` or `after` as argument.')
        if before is not None and after is not None:
            raise ValueError(
                'You cannot specify `before` and `after` arguments at the '
                'same time.')

        # determine new index
        if after is not None:
            new_index = self._fields.index(after) + 1
        elif before is not None:
            new_index = self._fields.index(before)

        return new_index

    def add_field(self, field, after=None, before=None):
        new_index = self._determine_new_index(after=after, before=before)
        new = self.copy()
        new._fields.insert(new_index, field)
        return new

    def move_field(self, field, after=None, before=None):
        current_index = self._fields.index(field)
        new_index = self._determine_new_index(after=after, before=before)
        new = self.copy()
        # insert into new place
        new._fields.insert(new_index, field)
        # remove current field
        if new_index < current_index:
            current_index += 1
        del new._fields[current_index]
        return new

    def remove_field(self, field):
        current_index = self._fields.index(field)
        new = self.copy()
        del new._fields[current_index]
        return new
