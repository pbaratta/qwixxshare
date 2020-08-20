from django.test import TestCase
from django.urls import reverse

class IndexViewTests(TestCase):
	def test_index_shows_up(self):
		response = self.client.get(reverse('qwixx:index'))
		self.assertContains(response, 'wixx', status_code=200)  # case insensitive lol

class RoomViewTests(TestCase):
	def get_room_view(self, room_name):
		return self.client.get(reverse('qwixx:room', kwargs={'room_name': room_name}))

	def test_room_name_entered(self):
		" the room name should appear on the page somewhere "
		room_name = "UNCOMMON_WORD_HERE"
		response = self.get_room_view(room_name)
		self.assertContains(response, room_name)

	def test_room_name_escape(self):
		" the room name should be escaped somehow so scripts can't appear "
		xss_room_name = "<script>alert('code');"
		response = self.get_room_view(xss_room_name)
		self.assertNotContains(response, xss_room_name)
