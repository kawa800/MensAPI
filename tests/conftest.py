import pytest
from unittest.mock import Mock
import requests
from pathlib import Path

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"

@pytest.fixture
def main_page() -> Page:
    """ Returns the Page object of the main Studierendenwerk Mensa Website"""
    website = Website(BASE_URL)
    return website.fetch("Index.html")

@pytest.fixture
def iframes() -> list[Page]:
    """ Returns the iFrames embedded in the Studierendenwerk Mensa Website """
    website = Website(BASE_URL)
    main_page = website.fetch("Index.html")
    return website.get_iframes(main_page)

@pytest.fixture
def mock_with_test_date() -> Mock:
    fake_html = """
        <td>
        <h2>Menuplan</h2>
        <p>31.08.2026</p>
        </td>
    """
    mock_response = Mock(spec=requests.Response)
    mock_response.text = fake_html 
    return mock_response

@pytest.fixture
def schweineschnitzel_mock() -> Mock:
    schweineschnitzel_html = Path("tests/fixtures/html/schweineschnitzel.html").read_text(encoding="utf-8")
    mock_response = Mock(spec=requests.Response)
    mock_response.text = schweineschnitzel_html 
    return mock_response

