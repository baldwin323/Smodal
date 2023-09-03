import pytest
from ..src.NLP import text_classification, entity_recognition, language_modeling

def test_text_classification():
    text = "Apple is a multinational technology company based in California."
    result = text_classification(text)
    assert "ORG" in result
    assert len(result) > 0

def test_entity_recognition():
    text = "Apple is a multinational technology company based in California."
    result = entity_recognition(text)
    assert ("Apple", "ORG") in result
    assert len(result) > 0

def test_language_modeling():
    text = "Apple is a multinational technology company based in California."
    result = language_modeling(text)
    assert "Apple" in result
    assert "is" not in result
    assert "." not in result
    assert len(result) > 0

if __name__ == "__main__":
    pytest.main()
