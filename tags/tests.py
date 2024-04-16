from django.db import transaction
from django.test import TestCase
from django.urls import reverse

# from django.test import SimpleTestCase

from tags.models import Tag


# Create your tests here.

class TagsTests(TestCase):

    @transaction.atomic
    def setUp(self) -> None:
        self.tag = Tag()
        self.tag.label = 'Romance Label'
        self.tag.save()
        self.createdTag = Tag.objects.create(label='Kitchen Utensils')
        print(self.createdTag)

    def test_home_page_exists(self) -> None:
        # response = self.client.get('/')
        # self.assertEqual(response.status_code, 200)
        pass

    def test_home_page_view_uses_correct_template(self):
        # res = self.client.get(reverse('home'))

        pass
    def test_home_page_view_url_by_name(self):
        pass
    def test__create_tag_created_tag_exists_in_db(self) -> None:
        tag_query_set = Tag.objects.filter(label='Romance Label')
        self.assertIsNotNone(tag_query_set)
        self.assertGreater(len(list(tag_query_set)), 0)
        self.assertEqual(len(list(tag_query_set)),2)

    def test_delete_tag_from_db_tag_does_not_exist(self) -> None:
        pass
        # self.createdTag.delete()

        # self.assert
        # self.assertIsNotNone(found_tag)

    def test_get_tag_from_db(self) -> None:
        found_tag = Tag.objects.get(pk=self.createdTag.id)
        self.assertIsNotNone(found_tag)
