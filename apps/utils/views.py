"""Util views."""

# Django REST Framework
from rest_framework import viewsets

class DynamicFieldView(viewsets.GenericViewSet):
    """
    Return fields base on action.
    Views that inherit from this one must declare a
    fields_to_return dict.
    """

    fields_to_return = {
        # Must follow the next format:
        #'action_name': () <- fields you want to return.
    }
    view_name = ''

    def get_serializer(self, *args, **kwargs):
        """Add fields to kwargs.

        handle wich fields must return base on action.
        """
        # if len(self.fields_to_return) < 1 or self.view_name.strip() == '':
        #     raise 'You must provide fields_to_return and view_name'
        for action in self.fields_to_return:
            if self.action == action:
                kwargs['fields'] = self.fields_to_return[action]
        return super(DynamicFieldView, self).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """Return serializer context."""
        context = super(DynamicFieldView, self).get_serializer_context()
        return context
