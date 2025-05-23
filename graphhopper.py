import requests

API_KEY = "3d6ceaf2-caba-43dc-84fa-7a1638f5e4ab"

def obtener_coordenadas(lugar):
    url = f"https://nominatim.openstreetmap.org/search?q={lugar},Chile&format=json"
    headers = {
        "User-Agent": "MiAppGraphHopper/1.0 (tu-email@dominio.com)"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error en geocodificación: código {response.status_code}")
        return None, None
    
    try:
        data = response.json()
    except Exception as e:
        print(f"Error al interpretar JSON: {e}")
        return None, None

    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        return None, None

while True:
    origen = input("Ciudad de origen (escribe q para salir): ")
    if origen.lower() == 'q':
        break
    destino = input("Ciudad de destino (escribe q para salir): ")
    if destino.lower() == 'q':
        break

    lat_origen, lon_origen = obtener_coordenadas(origen)
    lat_destino, lon_destino = obtener_coordenadas(destino)

    if None in (lat_origen, lon_origen, lat_destino, lon_destino):
        print("No se pudieron obtener las coordenadas de alguna ciudad, intenta con otro nombre.")
        continue

    url = (
        f"https://graphhopper.com/api/1/route?"
        f"point={lat_origen},{lon_origen}&point={lat_destino},{lon_destino}"
        f"&vehicle=car&locale=es&key={API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if 'message' in data:
            print("Error API:", data['message'])
            continue

        distancia_km = data['paths'][0]['distance'] / 1000
        duracion_ms = data['paths'][0]['time']

        segundos = duracion_ms / 1000
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos = int(segundos % 60)

        print(f"\n📍 Distancia: {distancia_km:.2f} km")
        print(f"⏱️ Duración: {horas}h {minutos}m {segundos}s\n")

    except Exception as e:
        print("❌ Error al consultar la API:", e)
