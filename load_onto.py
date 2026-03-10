import pathlib 
import rdflib

def list_directory_paths(path_folder:str) -> list[str]:
    """Retrieves a list of string file paths for all items within a specified directory."""
    return [str(path) for path in pathlib.Path(path_folder).iterdir()]

def generate_query_class()->str:
    """Generate SPARQL to retrieve Classes with labels and comments."""
    return """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?class_iri ?label_output ?comment_output where {
    VALUES ?classClass {owl:Class rdfs:Class} 
    ?class_iri rdf:type ?classClass.
    
    OPTIONAL {?class_iri rdfs:label ?label}
    OPTIONAL {?class_iri rdfs:comment ?comment}

    BIND(COALESCE(STR(?label), "") AS ?label_output)
    BIND(COALESCE(STR(?comment), "") AS ?comment_output) 

    FILTER(CONCAT(COALESCE(STR(?label), ""), " ", COALESCE(STR(?comment), "")) != " ")
} 
"""

def generate_query_predicate()->str:
    """Generate SPARQL to retrieve Classes with labels and comments."""
    return """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?prop_iri ?label_output ?comment_output ?domain ?range where {
    VALUES ?type {owl:FunctionalProperty owl:DatatypeProperty owl:Property rdf:Property owl:ObjectProperty }.
    ?prop_iri rdf:type ?type.
    
    OPTIONAL {?prop_iri rdfs:label ?label}
    OPTIONAL {?prop_iri rdfs:comment ?comment}

    BIND(COALESCE(STR(?label), "") AS ?label_output)
    BIND(COALESCE(STR(?comment), "") AS ?comment_output) 

    FILTER(CONCAT(COALESCE(STR(?label), ""), " ", COALESCE(STR(?comment), "")) != " ")

    OPTIONAL {?prop_iri rdfs:domain ?domain}
    BIND(COALESCE(STR(?domain), "None") AS ?domain) 
    OPTIONAL {?prop_iri rdfs:range ?range}
    BIND(COALESCE(STR(?range), "None") AS ?range) 
} 
"""

def retrieve_information_classes(path_folder:str, verbose=True):

    information_class = dict()
    ontologies_list = list_directory_paths(path_folder)

    for ontology_path in ontologies_list:
        if verbose:
            print(ontology_path)

        # Loading of the ontology
        g = rdflib.Graph()
        try:
            g.parse(ontology_path, format=ontology_path.split(".")[-1])
        except Exception as e:
            print(f"\tError parsing {ontology_path}: {e}")
            continue
    
        # Retrieval of Classes information
        cpt = 0
        for row in g.query(generate_query_class()):

            label = row.label_output.value
            # If no labels are found but a comment was given we retrieve a label from the URI
            if label == "":
                label = str(row.class_iri).split("/")[-1].split("#")[-1]

                # label = space_before_majuscule_loop(str(row.class_iri).split("/")[-1].split("#")[-1])

            information_class[str(row.class_iri)] = {"label":label,
                                                     "comment":row.comment_output.value,
                                                      "source":ontology_path}
            cpt +=1
        if verbose:
            print(f"\tClasses found:{cpt}")
            
    return information_class


def retrieve_information_predicates(path_folder:str, verbose=True):

    information_properties = dict()
    ontologies_list = list_directory_paths(path_folder)

    for ontology_path in ontologies_list:
        if verbose:
            print(ontology_path)

        # Loading of the ontology
        g = rdflib.Graph()
        try:
            g.parse(ontology_path, format=ontology_path.split(".")[-1])
        except Exception as e:
            print(f"\tError parsing {ontology_path}: {e}")
            continue
    
        # Retrieval of Classes information
        cpt = 0
        for row in g.query(generate_query_predicate()):

            label = row.label_output.value
            # If no labels are found but a comment was given we retrieve a label from the URI
            if label == "":
                label = str(row.prop_iri).split("/")[-1].split("#")[-1]

            information_properties[str(row.prop_iri)] = {"label":label,
                                                     "comment":row.comment_output.value,
                                                      "source":ontology_path}
            cpt +=1
        if verbose:
            print(f"\tProperties found:{cpt}")
            
    return information_properties