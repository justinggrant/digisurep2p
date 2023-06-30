from rest_framework import viewsets


class BaseGenericViewSet(viewsets.GenericViewSet):
    serializer_classes = {}

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes.get(self.action)

        return super().get_serializer_class()
