# config tests file
import pytest

# models
from quexl.apps.contact.models import Contact


@pytest.fixture
def create_contact(db):
    """create a contact instance"""
    contact = Contact()
    contact.full_name = "James Mwangi"
    contact.email = "james@app.com"
    contact.subject = "New Customer"
    contact.message = "Hello,... me and whatservices are available"
    contact.save()
    return contact


@pytest.fixture
def create_contact_with_errors(db):
    """create a contact instance"""
    contact = Contact()
    contact.email = "james@app.com"
    contact.subject = "New Customer"
    contact.save()
    return contact
