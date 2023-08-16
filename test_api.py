from Bio import Entrez

def get_species_taxonomy(species_names):
    Entrez.email = "seu_email@example.com"  # Substitua pelo seu e-mail registrado no NCBI

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

species_names = ["Bia actorion", "Archaeoprepona licomedes", "Archaeoprepona demophoon"]  # Substitua pelos nomes das espécies desejadas

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
    
    print("=" * 30)