from quexl.apps.authentication.validators import validate_possible_number
import pytest
from django.core.exceptions import ValidationError


def test_invalid_phone_number_validation():
    with pytest.raises(
        ValidationError, match="The phone number entered is not valid."
    ):
        validate_possible_number("0936")
