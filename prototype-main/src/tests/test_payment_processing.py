```python
import requests
import pytest
from src.exceptions import PaymentProcessingError
from src import payment_processing

def test_process_payment(mocker):
    mocker.patch('requests.post')

    requests.post.return_value.status_code = 200
    requests.post.return_value.json.return_value = {'transaction_id': '123456'}

    assert payment_processing.process_payment('user1', '50') == '123456'
    requests.post.assert_called_once()

    requests.post.return_value.status_code = 400
    with pytest.raises(PaymentProcessingError):
        payment_processing.process_payment('user1', '50')

    requests.post.assert_called()

def test_refund_payment(mocker):
    mocker.patch('requests.post')

    requests.post.return_value.status_code = 200
    requests.post.return_value.json.return_value = {'refund_id': '654321'}

    assert payment_processing.refund_payment('123456') == '654321'
    requests.post.assert_called_once()

    requests.post.return_value.status_code = 400
    with pytest.raises(PaymentProcessingError):
        payment_processing.refund_payment('123456')

    requests.post.assert_called()
```
