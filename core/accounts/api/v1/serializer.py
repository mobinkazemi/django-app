from rest_framework import serializers
from ...models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "repeat_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")
        if password != repeat_password:
            raise serializers.ValidationError({"details": "Passwords do not match."})

        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})  # type: ignore
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("repeat_password", None)
        return User.objects.create_user(**validated_data)  # type: ignore


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)

        validated_data["email"] = self.user.email  # type: ignore
        validated_data["user_id"] = self.user.id  # type: ignore

        return validated_data


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    repeat_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        repeat_new_password = attrs.get("repeat_new_password")
        if new_password != repeat_new_password:
            raise serializers.ValidationError(
                {"details": "New passwords do not match."}
            )

        try:
            validate_password(new_password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})  # type: ignore
        return super().validate(attrs)
