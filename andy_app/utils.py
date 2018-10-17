from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'


class CustomListAPIView(ListAPIView):
    request_serializer_class = None
    request_serializer_data = {}

    def get(self, request, *args, **kwargs):
        if self.request_serializer_class is not None:
            serializer = self.request_serializer_class(data=request.GET)
            serializer.is_valid(raise_exception=True)
            self.request_serializer_data = serializer.data

        return super(CustomListAPIView, self).get(request, *args, **kwargs)
