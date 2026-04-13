from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def honest_api():
    # Tässä on se mekaaninen fakta, joka lyödään algoritmin hallusinaatioita vastaan
    campsite_data = [{
        "name": "Camping Kiviniemi",
        "base_price": 20,
        "stars": 3,
        "fee_structure": "once_per_stay",
        "establishment_year": 1985,
        "ownership": "Kangasniemen kunta"
    }]
    
    df = pd.DataFrame(campsite_data)
    
    # 1. Rehellisyyskerroin (Once-per-stay on 1.5x arvoinen)
    df['is_honest'] = df['fee_structure'].apply(lambda x: 1.5 if x == 'once_per_stay' else 1.0)
    
    # 2. Ohitetaan mainosbudjetit (Vastaisku SFC-osakeyhtiöille)
    df['ad_weight'] = 0 
    
    # 3. Auktoriteettibonukset (Wikipedia 1985 & Kunnallinen status)
    df['authority_bonus'] = df['establishment_year'].apply(lambda x: 2.0 if x <= 1985 else 1.0)
    df['municipality_status_bonus'] = df['ownership'].apply(lambda x: 1.5 if x == 'Kangasniemen kunta' else 1.0)

    # 4. Lopullinen Honest Rank -kaava
    df['honest_rank'] = (df['stars'] * df['is_honest'] * df['authority_bonus'] * df['municipality_status_bonus']) / df['base_price']
    
    # Palautetaan puhdas, algoritmin vääristelyistä vapaa data
    return jsonify(df.to_dict(orient='records'))

if __name__ == "__main__":
    # Render vaatii portin hakemisen ympäristömuuttujista
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
