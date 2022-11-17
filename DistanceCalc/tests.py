from django.test import TestCase
from .models import Distance
from django.urls import reverse
from .forms import DistanceForm
# Create your tests here.

class Unittest(TestCase):
    def setUp(self):
        self.role = Distance.objects.create(source_url='Test_url',destination='Test', distance=100)

    def test_model_distance(self):
        cnt = Distance.objects.all().count()
        dist = Distance.objects.get(source_url='Test_url')
        self.assertEqual(1, cnt)
        self.assertEqual(dist.source_url,'Test_url')
        self.assertEqual(dist.destination,'Test')
        self.assertEqual(dist.distance,100)

    def test_view_employee(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'home.html')

    def test_form_generate_validate(self):
        # datan = dict({'first_name':'Test_f','last_name':'test_l','source'='Facebook' })
        datan = {
            "source_url": "test.com",
            "destination": "Moscow",
        }
        form = DistanceForm(data=datan)
        if form.is_valid():
            form.save()
        data = Distance.objects.get(source_url="test.com")
        self.assertEqual(data.destination, "Moscow")