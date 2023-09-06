```python
from django.test import TestCase
from .models import SaleItem, ChatBot

class SaleItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        SaleItem.objects.create(item_id="TestID", other_fields="Test")

    def test_item_id_label(self):
        saleitem = SaleItem.objects.get(id=1)
        field_label = saleitem._meta.get_field('item_id').verbose_name
        self.assertEqual(field_label, 'TestID')

    # Repeat the above test function for all fields and methods in SaleItem Model
   
class ChatBotModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ChatBot.objects.create(chat="Test Chat")

    def test_chat_content(self):
        chatbot = ChatBot.objects.get(id=1)
        field_label = chatbot._meta.get_field('chat').verbose_name
        self.assertEqual(field_label, 'Test Chat')

    # Repeat the above test function for all fields and methods in ChatBot Model

```