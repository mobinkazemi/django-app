from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import (
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
)
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import User


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        result = {
            "email": serializer.validated_data["email"],  # type: ignore
        }

        return Response(result, status=HTTP_201_CREATED)


class CustomAuthTokenView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "email": user.email, "user_id": user.pk})


class CustomAuthLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    pass


class ResetPasswordAPIView(UpdateAPIView):
    model = User
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):  # type: ignore
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        print(self.object)
        if serializer.is_valid():
            print(serializer.validated_data["old_password"])
            print(self.object.check_password(serializer.validated_data["old_password"]))
            if not self.object.check_password(serializer.validated_data["old_password"]):
                return Response(
                    {"details": "old password is not valid"},
                    status=HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.validated_data["new_password"])
            self.object.save()
            response = {
                "status": "success",
                "code": HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
