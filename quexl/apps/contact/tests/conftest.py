# config tests file
import os
import pytest

# models
from quexl.apps.contact.models import Contact



@pytest.fixture
def create_contact(db):
    """create a contact instance"""
    contact = Contact()
    contact.name = "James Mwangi"
    contact.email = "james@app.com"
    contact.title = "New Customer"
    contact.message = "Hello, I am new here and i need to know who can serve me and whatservices are available"
    contact.save()
    return contact

@pytest.fixture
def create_contact_with_errors(db):
    """create a contact instance"""
    contact = Contact()
    contact.email = "james@app.com"
    contact.title = "New Customer"
    contact.save()
    return contact


