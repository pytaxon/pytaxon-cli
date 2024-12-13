import requests
from pprint import pprint

def verificar_nomes_post(nomes_cientificos, data_sources="1", all_matches=False):
    url = "https://verifier.globalnames.org/api/v1/verifications"
    
    payload = {
        "nameStrings": nomes_cientificos,
        "dataSources": [
            1
        ],
        "withAllMatches": True,
        "withCapitalization": False,
        "withSpeciesGroup": False,
        "withUninomialFuzzyMatch": True,
        "withStats": False,
        "mainTaxonThreshold": 0.5
        }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

nomes = ["Nessaeae obrinus"]
resultado = verificar_nomes_post(nomes)

if resultado:
    print("Resultados da verificação:")
    pprint(resultado)
    # for nome, dados in zip(nomes, resultado.get("names", [])):
    #     print(f"\nNome: {nome}")
    #     print(f"Detalhes: {dados}")
else:
    print("Não foi possível verificar os nomes.")
