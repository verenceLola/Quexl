"""
test assign new user default regular user role
"""
from rolepermissions.roles import get_user_roles

from quexl.apps.roles.roles import RegularUserRole


def test_new_user_has_regular_user_role(create_db_user):
    """
    test new user has default user role
    """
    user = create_db_user
    assert RegularUserRole in get_user_roles(user)
