import pytest

from detector.analyzer import FEATURE_COLUMNS, extract_features, validate_url


@pytest.mark.parametrize("url", [
    "https://www.google.com",
    "http://example.com/path?x=1",
    "example.com",
    "http://192.168.0.1:8080/login",
])
def test_valid_urls(url):
    assert validate_url(url) is True


@pytest.mark.parametrize("url", [
    "",
    "not a url",
    "ftp://example.com",
    "https://localhost",
    None,
    123,
])
def test_invalid_urls(url):
    assert validate_url(url) is False


def test_trailing_slash_does_not_change_features():
    assert extract_features("https://example.com/") == extract_features("https://example.com")


def test_feature_columns_match():
    features = extract_features("https://example.com")

    assert list(features.keys()) == FEATURE_COLUMNS


def test_ip_detection():
    assert extract_features("http://192.168.0.1/login")["has_ip"] == 1
    assert extract_features("https://example.com")["has_ip"] == 0


def test_suspicious_words_detection():
    assert extract_features("https://example.com/login")["has_suspicious_words"] == 1
    assert extract_features("https://example.com/home")["has_suspicious_words"] == 0


def test_https_detection():
    assert extract_features("https://example.com")["has_https"] == 1
    assert extract_features("http://example.com")["has_https"] == 0