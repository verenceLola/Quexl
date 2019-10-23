"""
fixtures for profiles fields
"""
from quexl.apps.profiles.models import (
    Education,
    Skill,
    Address,
    WorkExperience,
    Language,
)
import pytest


@pytest.fixture()
def create_education(create_db_user):
    """
    create user education details
    """
    education_details = {
        "country": "ug",
        "description": "updated description",
        "course": "Computer Science",
        "school": "Multimedia University of Kenya",
        "level": "Degree",
        "start_date": "2019-10-25 22:58:55.216869+03",
        "end_date": "2019-10-25 16:58:55.216869+03",
        "on_going": "false",
    }
    profile = create_db_user.profile
    educ = Education.objects.create(profile=profile, **education_details)
    return educ


@pytest.fixture()
def create_skill(create_db_user):
    """
    create user skill info
    """
    profile = create_db_user.profile
    skill_details = {"name": "first", "expertise": "beginner"}
    skill = Skill.objects.create(profile=profile, **skill_details)
    return skill


@pytest.fixture()
def create_adress(create_db_user):
    """
    create user address info
    """
    profile = create_db_user.profile
    address_details = {
        "country": "tz",
        "street_address_1": "Site and Service",
        "city": "Nairobi",
        "city_area": "Kasarani",
        "postal_code": "50205",
        "country_area": "Nairobi",
        "phone": "+254713077520",
    }
    address = Address.objects.create(profile=profile, **address_details)
    return address


@pytest.fixture()
def create_workexperience(create_db_user):
    """
    create user work experience info
    """
    profile = create_db_user.profile
    work_details = {
        "country": "ug",
        "employee": "Andela Kenya",
        "role": "Software Developer",
        "start_date": "2019-10-25 22:58:55.216869+03",
        "end_date": "2019-10-25 16:58:55.216869+03",
        "on_going": "false",
        "description": "Should be optional",
    }
    work = WorkExperience.objects.create(profile=profile, **work_details)
    return work


@pytest.fixture()
def create_language(create_db_user):
    """
    create user education info
    """
    profile = create_db_user.profile
    language_details = {"name": "sw", "fluency": "limited"}
    return Language.objects.create(profile=profile, **language_details)
