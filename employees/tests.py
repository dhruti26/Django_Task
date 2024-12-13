from django.test import TestCase, Client
from django.urls import reverse
from .models import Employee
"""
TestCase: A Django class that provides an isolated test environment
Client: A test client to simulate requests and responses for views
reverse: Used to resolve URL names into actual URLs for testing
"""
class EmployeeViewsTest(TestCase):
    def setUp(self):
        """
        Setting up a test client and creating sample employee data
        """
        self.client = Client()
        self.employee = Employee.objects.create(
            name="Dhruti Desai",
            department="Software Engineering",
            email="dhr123@gmail.com",
            phone="9983218382"
        )
        self.list_url = reverse('employee_list')
        self.add_url = reverse('employee_create')  
        self.update_url = reverse('employee_update', args=[self.employee.id])
        self.delete_url = reverse('employee_delete', args=[self.employee.id])


    """
    Sends a GET request to the list
    Asserts that the response status code is 200(OK)
    Checks if the correct template (employee_list.html) is used.
    Verifies that the response contains the name of the sample employee
    """
    def test_employee_list_view(self):
        """Testing the employee list view"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/employee_list.html')
        self.assertContains(response, self.employee.name)

    def test_employee_create_view_get(self):
        """Test the employee create view for GET request"""
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/employee_form.html')

    def test_employee_create_view_post(self):
        """Test the employee create view for POST request."""
        data = {
            'name': 'John Smith',
            'department': 'Developer',
            'email': 'john@gmail.com',
            'phone': '9876543210'
        }
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(Employee.objects.filter(name='John Smith').exists())

    def test_employee_update_view_get(self):
        """Test the employee update view for GET request."""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/employee_form.html')

    def test_employee_update_view_post(self):
        """Test the employee update view for POST request."""
        data = {
            'name': 'Rahul',
            'department': 'IT',
            'email': 'rahul@gmail.com',
            'phone': '1122334455'
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, 'Rahul')
        self.assertEqual(self.employee.department, 'IT')

    def test_employee_delete_view_get(self):
        """Test the employee delete view for GET request."""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/employee_confirm_delete.html')

    def test_employee_delete_view_post(self):
        """Test the employee delete view for POST request."""
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())
        
        # ensuring that the deleted employee no longer appears in the employee list
        response = self.client.get(self.list_url)
        self.assertNotContains(response, self.employee.name)
