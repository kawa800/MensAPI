from fastapi import FastAPI
from fastapi.testclient import TestClient
from scraper.scraper import get_day 

def test_get_day():
    print("test")
