import json
import math
from database import SessionLocal, engine
from tables import Recipe, Base

def load():
    Base.metadata.create_all(bind=engine)
    with open('US_recipes_null.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    recipes_list = data.values() if isinstance(data, dict) else data

    with SessionLocal() as db:
        for item in recipes_list:
            for key, value in item.items():
                if isinstance(value, float) and math.isnan(value):
                    item[key] = None
            
            n_recipe = Recipe(
                cuisine=item.get("cuisine"),
                title=item.get("title"),
                rating=item.get("rating"),
                prep_time=item.get("prep_time"),
                cook_time=item.get("cook_time"),
                total_time=item.get("total_time"),
                description=item.get("description"),
                nutrients=item.get("nutrients"), 
                serves=item.get("serves")
            )
            db.add(n_recipe)
        db.commit()

if __name__ == "__main__":
    load()