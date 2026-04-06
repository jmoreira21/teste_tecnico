
import requests
from datetime import datetime
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_API = "https://api.open-meteo.com/v1/forecast"

def obter_coordenadas(cidade):

    try:
        params = {
            "name": cidade,
            "count": 10,
            "language": "pt",
            "format": "json"
        }
        response = requests.get(GEOCODING_API, params=params, timeout=10, verify=False)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("results"):
            return None
        
        resultado = data["results"][0]
        return {
            "latitude": resultado["latitude"],
            "longitude": resultado["longitude"],
            "nome": resultado.get("name", cidade),
            "estado": resultado.get("admin1", ""),
            "pais": resultado.get("country", "")
        }
    
    except requests.exceptions.ConnectionError:
        print(f"Erro de conexão: Verifique sua conexão com a internet")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de rede: {str(e)[:100]}")
        return None
    except Exception as e:
        print(f"Erro ao processar: {str(e)[:100]}")
        return None

def obter_previsao(latitude, longitude):

    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto",
            "forecast_days": 7
        }
        response = requests.get(FORECAST_API, params=params, timeout=10, verify=False)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        print(f"Erro de conexão: Verifique sua conexão com a internet")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de rede: {str(e)[:100]}")
        return None
    except Exception as e:
        print(f"Erro ao processar: {str(e)[:100]}")
        return None

def calcular_estatisticas(temps_max, temps_min):
    if not temps_max or not temps_min:
        return None, None, None
    
    media_max = sum(temps_max) / len(temps_max)
    media_min = sum(temps_min) / len(temps_min)
    media_geral = (media_max + media_min) / 2
    
    temp_max_periodo = max(temps_max)
    temp_min_periodo = min(temps_min)
    
    return media_geral, temp_max_periodo, temp_min_periodo

def exibir_previsao(cidade_info, previsao_data):

    print("\n" + "=" * 50)
    print(f"Previsão para: {cidade_info['nome']}, {cidade_info['estado']}")
    print("=" * 50)
    
    datas = previsao_data["daily"]["time"]
    temps_max = previsao_data["daily"]["temperature_2m_max"]
    temps_min = previsao_data["daily"]["temperature_2m_min"]
    
    media, max_periodo, min_periodo = calcular_estatisticas(temps_max, temps_min)
    
    data_inicio = datetime.strptime(datas[0], "%Y-%m-%d").strftime("%d/%m/%Y")
    data_fim = datetime.strptime(datas[-1], "%Y-%m-%d").strftime("%d/%m/%Y")
    
    print(f"Período: {data_inicio} a {data_fim}")
    print(f"Temperatura média: {media:.1f}°C")
    print(f"Máxima do período: {max_periodo:.1f}°C ({datas[temps_max.index(max_periodo)]})")
    print(f"Mínima do período: {min_periodo:.1f}°C ({datas[temps_min.index(min_periodo)]})")
    print("-" * 50)
    
    for i, data in enumerate(datas):
        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m")
        print(f"{data_formatada} Min: {temps_min[i]:.1f}°C Max: {temps_max[i]:.1f}°C")
    
    print("=" * 50)

def main():
    
    while True:
        try:
            cidade = input("Digite o nome da cidade: ").strip()
            
            if not cidade:
                print("Digite um nome valido\n")
                continue
            
            print(f"\nBuscando coordenadas para '{cidade}'")
            cidade_info = obter_coordenadas(cidade)
            
            if not cidade_info:
                print(f"Cidade '{cidade}' não encontrada. Tente novamente.\n")
                continue
            
            print(f"Latitude: {cidade_info['latitude']:.4f} | Longitude: {cidade_info['longitude']:.4f}")
            
            previsao = obter_previsao(cidade_info["latitude"], cidade_info["longitude"])
            
            if not previsao:
                print("Erro ao obter previsão. Tente novamente.\n")
                continue
            
            exibir_previsao(cidade_info, previsao)
            
            while True:
                resposta = input("\n Deseja consultar outra cidade? (s/n): ").strip().lower()
                if resposta in ["s", "sim"]:
                    print()
                    break
                elif resposta in ["n", "nao"]:
                    print("\nSaindo\n")
                    return
                else:
                    print("Resposta inválida. Digite 's' ou 'n'.")
        
        except KeyboardInterrupt:
            print("\n\nPrograma encerrado\n")
            sys.exit(0)
        except EOFError:
            print("\nPrograma encerrado\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
