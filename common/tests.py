from django.test import TestCase
from unittest.mock import patch
from django.urls import path
from django.urls import reverse


class TestRedis(TestCase):
    def test_redis_health_check(self):
        with patch('common.redis_client.p', return_value=True):
            response = self.client.get(reverse('health_check_redis'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b'OK')
            self.assertEqual(response['Content-Type'], 'text/plain')
            
        with patch('common.redis_client.p', return_value=False):
            response = self.client.get(reverse('health_check_redis'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b'ERROR')
            self.assertEqual(response['Content-Type'], 'text/plain')    
 