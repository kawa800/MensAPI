from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

class Page:

    def __init__(self, url: str, response: requests.Response, parser: str = "html.parser"):
        self.url = url
        self.response = response
        self.soup = BeautifulSoup(response.text, parser)

    @property
    def title(self) -> str | None:
        tag = self.soup.select_one("title")
        return tag.get_text().strip() if tag else None

    @property
    def day(self) -> str | None:
        day = self.soup.find("h2")
        return day.get_text().strip() if day else None
    
    @property
    def date(self) -> str | None: 
        date = self.soup.find("h2").find_next_sibling("p")
        return date.get_text().strip() if date else None

    @property
    def meals(self) -> list[str] | None:
        res = []
        meal_list = self.soup.find_all("div", class_="container")
        for meal in meal_list:
            meal  = meal.text.strip()
            print(meal)
            meal_cleaned = " mit ".join(meal.split("\n"))
            if meal_cleaned:
                res.append(meal_cleaned)

        return res if res else None

    @property
    def prices(self) -> list[dict[str, float]]:
        res = []
        meals = self.soup.find_all("table", class_="article-component-header")
        for meal in meals:
            prices_cells = meal.find_all("td")
            meal_name = prices_cells[0].get_text().strip()
            student_price = prices_cells[1].get_text().strip().split(" ")[1]
            nonstudent_price = prices_cells[2].get_text().strip().split(" ")[3]
            res.append({"Meal": meal_name, "Students": float(student_price.replace(",", ".")), "Non-Students": float(nonstudent_price.replace(",", "."))})
        return res

    @property
    def nutrients(self) -> list[dict[str,float]]:
        res = []
        values = []
        keys = [
            "Protein",
            "Fat",
            "Saturated Fat",
            "kcal",
            "kJ",
            "Carbohydrates",
            "Salt",
            "Sugar",
        ]
    
        nutrient_table = self.soup.find_all("table", class_="nutrienttable")

        nutrient_values = []
        for tables in nutrient_table[::2]:
            # [start:stop:increment]
            nutrient_values.append(tables.find_all("td", class_="nutrient_value"))

        print(nutrient_values)
        values = []
        for nutrients in nutrient_values:
            for value in nutrients:
                v = value.get_text().strip()
                v = v.replace(",",".")
                v = float("".join([char for char in v if char.isdigit() or char == "."]))
                if v:
                    values.append(v)

        for i in range(0, len(values), len(keys)):
            chunk = values[i:i + len(keys)]
            res.append(dict(zip(keys, chunk)))

        return res

    def select(self, css_selector: str):
        return self.soup.select(css_selector)
    
    def __repr__(self):
        return f"url: {self.url}, status: {self.response.status_code}, title: {self.title}"
