from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):

    def test_dashboard_view_status_code(self):
        # Act
        response = self.client.get(reverse("dashboard"))
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template_used(self):
        # Act
        response = self.client.get(reverse("dashboard"))
        # Assert
        self.assertTemplateUsed(response, "dashboard.html")

    def test_dashboard_content(self):
        # Act
        response = self.client.get(reverse("dashboard"))
        # Assert
        self.assertContains(response, "<h1>Weather Dashboard</h1>")
        self.assertContains(response, 'href="/static/css/main.css"')
        self.assertContains(response, 'src="/static/js/dashboard.js"')
