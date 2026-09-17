""" Match NUMBER.png to allergen or additive name in the legend. The website uses no clear ordering """

ALLERGENS_BY_IMAGE = {
    15: "sulphites",
    12: "milk",
    8: "gluten",
    19: "soy",
    16: "celery",
    20: "wheat",
    13: "rye",
    7: "barley",
    17: "mustard",
    18: "sesame",
}

ADDITIVES_BY_IMAGE = {
    14: "beef",
    4: "pork",
    11: "preservative",
    5: "antioxidant",
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
