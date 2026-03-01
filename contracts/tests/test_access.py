from django.test import TestCase, Client
from django.urls import reverse

class AccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public_solicitation_is_accessible(self):
        """Test that the public solicitation form is accessible without login."""
        response = self.client.get(reverse('public-solicitation'))
        self.assertEqual(response.status_code, 200)
    
    def test_solicitation_success_is_accessible(self):
        """Test that the solicitation success page is accessible without login."""
        response = self.client.get(reverse('solicitation-success'))
        self.assertEqual(response.status_code, 200)

    def test_contract_list_redirects_to_login(self):
        """Test that the contract list view redirects to admin login if not authenticated."""
        response = self.client.get(reverse('contract-list'))
        self.assertRedirects(response, f"/admin/login/?next={reverse('contract-list')}")

    def test_contract_create_redirects_to_login(self):
        """Test that the contract creation view redirects to admin login if not authenticated."""
        response = self.client.get(reverse('contract-create'))
        self.assertRedirects(response, f"/admin/login/?next={reverse('contract-create')}")
