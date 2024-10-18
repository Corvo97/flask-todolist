import requests
from flask import request

def get_city_from_ip():
    # Consultando API da GeoJS
    response = requests.get(f"https://get.geojs.io/v1/ip/geo/{request.remote_addr}.json")

    if response.status_code == 200:
        data = response.json()
        cidade = data.get('city')
        pais = data.get('country')
        return f'{cidade}, {pais}'
    else:
        return jsonify({'erro': 'Não foi possível obter a localização'}), 500

