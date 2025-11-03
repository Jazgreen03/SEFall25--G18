from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from Organization.models import Organization

User = get_user_model()

orgName = "Organization"
orgNameTwo = "Org"

valid_orgType = "foodbank"
invalid_orgType = "hospital"

orgLocation = "NC State University"
orgLocationTwo = "UNC Chapel Hill"


class TestOrganizationModel(TestCase):

    # Creates a user with the location permission for testing purposes
    def setUp(self):
        self.user = User.objects.create(
            username="orgUser",
            email="org@email.com",
            password="123abc"
        )
        self.user.role = "location"
        self.user.save()

    # Create an Organization and verify the Inventory was created
    def test_valid_Org_create(self):
        Organization.objects.createOrganization(name=orgName, orgType=valid_orgType, location=orgLocation, user=self.user)

        org = Organization.objects.filter(name=orgName).first()

        self.assertEqual(org.name, orgName)
        self.assertEqual(org.orgType, valid_orgType)
        self.assertEqual(org.location, orgLocation)

        self.assertIsNotNone(org.inv)

    # Attempt to create Organization with invalid parameters
    def test_invalid_Org_create(self):

        # Create the valid organization first
        Organization.objects.createOrganization(name=orgName, orgType=valid_orgType, location=orgLocation, user=self.user)

        # Check that a duplicate name organization isn't allowed
        with self.assertRaises(IntegrityError):
            Organization.objects.createOrganization(name=orgName, orgType=valid_orgType, location=orgLocationTwo, user=self.user)

        # Check that a duplication location isn't allowed
        with self.assertRaises(IntegrityError):
            Organization.objects.createOrganization(name=orgNameTwo, orgType=valid_orgType, location=orgLocation, user=self.user)

        # Check that invalid types aren't allowed
        with self.assertRaises(ValidationError):
            Organization.objects.createOrganization(name=orgNameTwo, orgType=invalid_orgType, location=orgLocationTwo, user=self.user)