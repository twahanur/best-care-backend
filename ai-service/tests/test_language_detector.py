import pytest
from app.query.language_detector import language_detector

def test_detect_english():
    assert language_detector.detect("Show me all available luxury cars in Dhaka") == "english"
    assert language_detector.detect("What is the security deposit for Toyota Prado?") == "english"

def test_detect_bangla_unicode():
    assert language_detector.detect("খুলনায় কি কি গাড়ি অ্যাভেইলেবল আছে?") == "bangla"
    assert language_detector.detect("৪ তারিখের জন্য একটা এসইউভি বুক করতে চাই") == "bangla"

def test_detect_banglish():
    assert language_detector.detect("Khulna theke dhaka te agamikal SUV book koro") == "banglish"
    assert language_detector.detect("amk 4 tarik ekta car book koro") == "banglish"
    assert language_detector.detect("sajek jabo kon gari bhalo hobe?") == "banglish"
    assert language_detector.detect("amar booking status dekhao") == "banglish"
