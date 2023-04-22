import os
from django.utils.crypto import get_random_string
from django.utils.translation import activate

from account.mail import Mail


def send_verification_code(*args, **kwargs):
    code = get_random_string(length=4, allowed_chars="1234567890")

    context = dict()
    context["type"] = "verification"
    context["code"] = code
    context["ref_number"] = "Code_" + str(code)
    response = Mail.send_verification_email(
        kwargs["email"], context
    )
    # activate(LANGUAGE_CODE)
    return code if response else None
