import pytest

from detector.predictor import is_trusted, predict_url


def test_prediction_result_structure():
    result = predict_url("https://example.com")

    assert set(result.keys()) >= {"url", "prediction", "confidence", "reason"}
    assert result["prediction"] in {"Legitimate", "Phishing"}
    assert 0 <= result["confidence"] <= 100


@pytest.mark.parametrize("url", [
    "https://academico.uerr.edu.br/aluno",
    "https://www.youtube.com/",
    "https://github.com/user/repo",
])
def test_trusted_urls_skip_model(url):
    result = predict_url(url)

    assert result["prediction"] == "Legitimate"
    assert result["confidence"] is None
    assert result["reason"] == "Trusted domain"


@pytest.mark.parametrize("url", [
    "https://example.com",
    "http://192.168.0.1/login",
    "https://youtube.com.fake-site.xyz",
])
def test_untrusted_urls_are_not_allowlisted(url):
    assert is_trusted(url) is False


@pytest.mark.parametrize("url", [
    "not a url",
    "",
    "ftp://example.com",
    "https://",
    "https://-invalid-.com",
])
def test_invalid_urls_raise_error(url):
    with pytest.raises(ValueError):
        predict_url(url)