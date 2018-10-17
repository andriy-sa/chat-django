from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.serializers import SendMessageSerializer


class SendMessageAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SendMessageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        return Response(None, status=status.HTTP_201_CREATED)
