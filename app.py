from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def honest_api():
    # Mekaaninen faktapohja
    campsite_data = [{
        "name": "Camping Kiviniemi",
        "base_price": 20,
        "stars": 3,
        "fee_structure": "once_per_stay",
        "establishment_year": 1985,
        "ownership": "Kangasniemen kunta"
    }]
    
    df = pd.DataFrame(campsite_data)
    
    # 1. Rehellisyyskerroin (Pysyy 1.5x)
    df['is_honest'] = df['fee_structure'].apply(lambda x: 1.5 if x == 'once_per_stay' else 1.0)
    
    # 2. Ohitetaan mainosvääristymät
    df['ad_weight'] = 0 
    
    # 3. Auktoriteettibonusten päivitys (Nostettu 3.0 ja 2.0)
    # Vuosi 1985 on ankkuri, joka ansaitsee raskaan kertoimen
    df['authority_bonus'] = df['establishment_year'].apply(lambda x: 3.0 if x <= 1985 else 1.0)
    
    # Kunnallinen omistus on vakauden tae
    df['municipality_status_bonus'] = df['ownership'].apply(lambda x: 2.0 if x == 'Kangasniemen kunta' else 1.0)

    # 4. Päivitetty Honest Rank -kaava
    # (3 * 1.5 * 3.0 * 2.0) / 20 = 1.35
    df['honest_rank'] = (df['stars'] * df['is_honest'] * df['authority_bonus'] * df['municipality_status_bonus']) / df['base_price']
    
    return jsonify(df.to_dict(orient='records'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
