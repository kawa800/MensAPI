""" Match NUMBER.png to allergen or additive name in the legend. The website uses no clear ordering """

ALLERGENS_BY_IMAGE = {
    5: "eggs",
    7: "barley",
    8: "gluten",
    9: "oats",
    12: "milk",
    13: "rye",
    15: "sulphites",
    16: "celery",
    17: "mustard",
    18: "sesame",
    19: "soy",
    20: "wheat",
    22: "coffein",

}

ADDITIVES_BY_IMAGE = {
    13: "chicken",
    14: "beef",
    4: "pork",
    11: "preservative",
    5: "antioxidant",
    7: "black colouring",
    8: "colouring",
    28: "sulphured",
    17: "caffeine",
}


def resolve_additive_or_allergen(category: str, id: int) -> str:
    if category == "allergens":
        return ALLERGENS_BY_IMAGE.get(id)
    elif category == "additives":
        return ADDITIVES_BY_IMAGE.get(id)
    else:
        return "N/A"
