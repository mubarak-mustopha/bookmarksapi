import re


def validate_username(username):
    if not re.match(r"^\w+$", username, re.I):
        raise serializers.ValidationError(
            "Username can contain only alphanumeric characters and underscore."
        )
