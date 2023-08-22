from Bio import Entrez
import json
from pprint import pprint

Entrez.email = "seu_email@example.com"

def get_species_taxonomy(species_names):
    taxonomies = []

    for species_name in species_names:
        handle = Entrez.esearch(db="taxonomy", term=species_name)
        record = Entrez.read(handle)
        handle.close()

        if record["Count"] == "0":
            taxonomies.append({"species_name": species_name, "taxonomy": None})
            continue

        tax_id = record["IdList"][0]
        handle = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
        taxonomy_data = Entrez.read(handle)[0]
        handle.close()

        taxonomies.append({"species_name": species_name, "taxonomy": taxonomy_data})

    return taxonomies

def get_specie_taxonomy(specie_name):
    handle = Entrez.esearch(db="taxonomy", term=specie_name)
    record = Entrez.read(handle)
    handle.close()

    tax_id = record["IdList"][0]
    handle = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
    taxonomy_data = Entrez.read(handle)[0]
    handle.close()

    # print(json.dumps(record, indent=4))
    print(json.dumps(taxonomy_data, indent=4))

get_specie_taxonomy("Bia actorion")

'''species_names = ["Bia actorion", "Archaeoprepona licomedes", "Archaeoprepona demophoon"]  # Substitua pelos nomes das espécies desejadas

taxonomy_data = get_species_taxonomy(species_names)

for data in taxonomy_data:
    species_name = data["species_name"]
    taxonomy = data["taxonomy"]
    
    print(f"Espécie: {species_name}")
    if taxonomy:
        print(f"Taxonomia: {taxonomy['ScientificName']}")
        print(f"Linhagem: {taxonomy['Lineage']}")
        # Outras informações taxonômicas podem ser acessadas aqui
    else:
        print("Espécie não encontrada na base de dados.")
    
    print("=" * 30)'''

