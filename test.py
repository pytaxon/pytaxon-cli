import requests

def verificar_nomes_post(nomes_cientificos, data_sources="1|12", all_matches=False):
    url = "https://verifier.globalnames.org/api/v1/verifications"
    
    payload = {
        "nameStrings": [
            "Pomatomus soltator",
            "Bubo bubo (Linnaeus, 1758)",
            "Isoetes longissimum"
        ],
        "dataSources": [
            1,
            12,
            170
        ],
        "withAllMatches": False,
        "withCapitalization": False,
        "withSpeciesGroup": False,
        "withUninomialFuzzyMatch": False,
        "withStats": True,
        "mainTaxonThreshold": 0.6
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

nomes = ["Pomatomus saltator", "Bubo bubo", "Isoetes longissimum"]
resultado = verificar_nomes_post(nomes)

if resultado:
    print("Resultados da verificação:")
    for nome, dados in zip(nomes, resultado.get("names", [])):
        print(f"\nNome: {nome}")
        print(f"Detalhes: {dados}")
else:
    print("Não foi possível verificar os nomes.")
