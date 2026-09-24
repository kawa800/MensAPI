import pytest
from unittest.mock import Mock
import requests
from pathlib import Path
from typing import TypedDict
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
import datetime as dt

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 
from mensapi.scraper.legend import resolve_additive_or_allergen
from mensapi.scraper.types import DailyMenu
from mensapi.api.main import app, Base, get_db

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"
HTML_DIR = Path(__file__).parent / "fixtures" / "html"

# Set up fake database
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def db_setup():
    Base.metadata.create_all(bind=engine)
    yield # The test runs
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def iframes() -> list[Page]:
    """ Returns the iFrames embedded in the Studierendenwerk Mensa Website on the 08.09.2026 """
    website = Website.from_mensa_url(BASE_URL)
    return website.iframes

def _construct_mock(html: str) -> Page:
    mock_response = Mock(spec=requests.Response)
    mock_response.content = html 
    page = Page("https://example.com", response=mock_response)
    return page 
    
@pytest.fixture
def mock_with_test_date() -> Page:
    fake_html = """
        <td>
        <h2>Menuplan</h2>
        <p>31.08.2026</p>
        </td>
    """
    return _construct_mock(fake_html)

@pytest.fixture
def schweineschnitzel_mock() -> Page:
    schweineschnitzel_html = (HTML_DIR/ "schweineschnitzel.html").read_text(encoding="utf-8")
    return _construct_mock(schweineschnitzel_html)

@pytest.fixture
def curryvurst_mock() -> Page:
    curryvurst_html = (HTML_DIR / "curryvurst.html").read_text(encoding="utf-8")
    return _construct_mock(curryvurst_html)

@pytest.fixture
def curryvurst_expected_nutrients() -> list[dict[str,str]]:
    expected_nutrients = [
        {
            "Protein": 17.84,
            "Fat": 30.53,
            "Saturated Fat": 5.13,
            "kcal": 850.65,
            "kJ": 3569.38,
            "Carbohydrates": 120.62,
            "Salt": 7.59,
            "Sugar": 7.25,
        },
        {
            "Protein": 17.04,
            "Fat": 67.63,
            "Saturated Fat": 11.59,
            "kcal": 1143.68,
            "kJ": 4801.19,
            "Carbohydrates": 112.11,
            "Salt": 5.84,
            "Sugar": 28.91,
        },
        {
            "Protein": 18.87,
            "Fat": 14.72,
            "Saturated Fat": 1.54,
            "kcal": 444.59,
            "kJ": 1863.99,
            "Carbohydrates": 53.73,
            "Salt": 6.63,
            "Sugar": 8.68,
        },
    ]
    return expected_nutrients

@pytest.fixture
def bolognese_mock() -> Page:
    bolognese_html = (HTML_DIR/ "sauce_bolognese.html").read_text(encoding="utf-8")
    return _construct_mock(bolognese_html)
 
@pytest.fixture
def bolognese_expected_allergens() -> list[dict[str,str]]:
    expected_allergens = [
        {
            "allergen_id": "8",
            "category": "allergens",
            "name": "gluten",
        },
        {
            "allergen_id": "16",
            "category": "allergens",
            "name": "celery", 
        },
        {
            "allergen_id": "20",
            "category": "allergens",
            "name": "wheat",
        },
        {
            "allergen_id": "14",
            "category": "additives",
            "name": "beef",
        },
    ]
    return expected_allergens


@pytest.fixture
def complete_dishes_bolognese() -> DailyMenu:
    result = {
        "day": "Donnerstag",
        "date": dt.datetime(2026, 9, 10, 0, 0),
        "name": "Penne mit Sauce Bolognese",
        "price": {
            "Students": 2.40,
            "Non-Students": 4.50,
        },
        "nutrients": {
            "Protein": 26.4,
            "Fat": 25.53,
            "Saturated Fat": 6.42,
            "kcal": 734.85,
            "kJ": 3085.65,
            "Carbohydrates": 97.22,
            "Salt": 3.68,
            "Sugar": 11.77,
        },
        "allergens": [
            {
                "allergen_id": "8",
                "category": "allergens",
                "name": "gluten", 
            },
            {
                "allergen_id": "16",
                "category": "allergens",
                "name": "celery",
            },
            {
                "allergen_id": "20",
                "category": "allergens",
                "name": "wheat",
            },
            {
                "allergen_id": "14",
                "category": "additives",
                "name": "beef",
            },
        ],
    }
    return result
