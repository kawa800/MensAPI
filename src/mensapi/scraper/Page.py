from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re
import datetime as dt

from mensapi.scraper.types import DailyMenu
from mensapi.scraper.legend import resolve_additive_or_allergen

class Page:

    def __init__(self, url: str, response: requests.Response, parser: str = "html.parser"):
        """ Page requires a Response to be instantiated, because """
        self.url = url
        self.response = response
        self.soup = BeautifulSoup(response.content, parser)


    @property
    def containers(self) -> list[str]:
        """
        A container is the parent that contains all the information needed to parse a dish, as well as excess information.
        It is made up of: button.accordion (contains meal name, prices) and sibling div.panel (contains nutrients, allergens).
        """
        # filter
        node = self.soup.find_all("button", class_="accordion")
        res = []
        for n in node:
            component = n.find("table", class_="article-component-header")
            if component:
                res.append(n)
                res.append(n.find_next_sibling("div", class_="panel"))

        return res
        

    @property
    def title(self) -> str | None:
        tag = self.soup.select_one("title")
        return tag.get_text().strip() if tag else None

    @property
    def day(self) -> str | None:
        day = self.soup.find("h2")
        return day.get_text().strip() if day else None
    
    @property
    def date(self) -> dt.datetime | None: 
        date = self.soup.find("h2").find_next_sibling("p").text
        format = "%d.%m.%Y"
        res = dt.datetime.strptime(date, format)
        return res if res else None

    @property
    def meal_name(self) -> list[str] | None:
        res = []
        meal_list = self.soup.find_all("button", class_="accordion")
        for meal in meal_list:
            first_td = meal.find("td")
            if first_td:
                res.append(first_td.text)
            # for name in names:
            #     meal  = name.text.strip()
            #     meal_cleaned = " ".join(meal.split("\n"))
            #     if meal_cleaned:
            #         res.append(meal_cleaned)

        return res if res else None


    @property
    def meals(self) -> list[str] | None:
        res = []
        meal_list = self.soup.find_all("div", class_="container")
        for meal in meal_list:
            meal  = meal.text.strip()
            meal_cleaned = " mit ".join(meal.split("\n"))
            if meal_cleaned:
                res.append(meal_cleaned)

        return res if res else None

    @property
    def prices(self) -> list[dict[str, float | str]]:
        res = []
        meals = self.soup.find_all("table", class_="article-component-header")
        for meal in meals:
            prices_cells = meal.find_all("td")
            student_price = prices_cells[1].get_text().strip().split(" ")[1]
            nonstudent_price = prices_cells[2].get_text().strip().split(" ")[3]
            res.append({"Students": float(student_price.replace(",", ".")), "Non-Students": float(nonstudent_price.replace(",", "."))})
        return res

    @property
    def nutrients(self) -> list[dict[str,float]]:
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
            nutrient_values.append(tables.find_all("td", class_="nutrient_value"))

        values = []
        for nutrients in nutrient_values:
            for value in nutrients:
                v = value.get_text().strip()
                v = v.replace(",",".")
                v = float("".join([char for char in v if char.isdigit() or char == "."]))
                if v:
                    values.append(v)

        res = []
        for i in range(0, len(values), len(keys)):
            slice = values[i:i + len(keys)]
            res.append(dict(zip(keys, slice)))

        return res

    @property
    def allergens_and_additives(self) -> list[dict[str,str]]:
        result = []
        dishes = self.soup.find_all("div", class_="menuitem")

        for dish in dishes: 
            r = []
            for image in dish.select("td.sectionheader + td img, tr:has(td.sectionheader) + tr img"): 
                src = image.get("src").replace("\\","/")
                if src:
                    category, image_name = src.split("/")[1:]
                    allergen_id = image_name.split(".")[0]
                    name = resolve_additive_or_allergen(category, int(allergen_id))

                    if name is None:
                        raise ValueError(f"Name resolution failed for: {dish}")


                    r.append({
                        "allergen_id": allergen_id,
                        "category": category,
                        "name": name
                    })

            result.append(r)

        return result

    @property
    def complete_dishes(self) -> DailyMenu:
        meals = self.meals
        prices = self.prices
        nutrients = self.nutrients
        allergens = self.allergens_and_additives

        dishes = []
        if meals:
            for i, name in enumerate(meals):
                dishes.append({
                    "day": self.day,
                    "date": self.date,
                    "name": name, 
                    "price": prices[i],
                    "nutrients": nutrients[i],
                    "allergens": allergens[i], 
                })

        return dishes


    def select(self, css_selector: str):
        return self.soup.select(css_selector)
    
    def __repr__(self):
        status = self.response.status_code if self.response else None
        return f"Page(url={self.url!r}, status={self.response.status_code!r}, day={self.day!r}, date={self.date!r}, title={self.title!r}"
