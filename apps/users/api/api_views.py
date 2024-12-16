from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.users.api.service import create_author
from apps.users.serializers import AuthorRegisterSerializers


class AuthorRegisterAPIView(GenericAPIView):
    """ Api for registering Author"""

    permission_classes = (AllowAny,)
    serializer_class = AuthorRegisterSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = create_author(serializer.validated_data)
        return response


###### HERE WE CAN ALSO SPECIFY LOGIN API AND GIVE TOKEN MANUALLY BUT I'M DIRECTLY USING JWT ######
