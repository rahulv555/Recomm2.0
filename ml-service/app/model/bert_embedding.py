import pandas as pd

def safe(x):
    return "" if pd.isna(x) else str(x)

def build_user_text_groups(row):
    lifestyle = " ".join(filter(None, [
        f"Smoker : {row['smoker']},",
        f"Drink level : {row['drink_level']},",
        f"Transport : {row['transport']},",
        f"Activity : {row['activity']},",
    ]))

    social = " ".join(filter(None, [
        f"Marital status : {row['marital_status']},",
        f"Hijos : {row['hijos']},",
        f"Personality : {row['personality']},",
        f"Interest : {row['interest']},",
        f"Religion : {row['religion']},",
    ]))

    preference = " ".join(filter(None, [
        f"Dress pref : {row['dress_preference']},",
        f"Ambience : {row['ambience']},",
        f"Budget : {row['budget']},",
    ]))

    print(row['rcuisine'])
    cuisine = " ".join(row['rcuisine']) if isinstance(row['rcuisine'], list) else ""
    cuisine = f"Cuisine : {cuisine}"

    return lifestyle, social, preference, cuisine