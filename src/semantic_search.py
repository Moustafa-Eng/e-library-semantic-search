import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
import os


class ELibrarySemanticSearch:
    def __init__(self, ontology_path, data_path):
        """Initialize the semantic search engine with ontology and data paths."""
        self.graph = Graph()

        # Load ontology and data
        print(f"Loading ontology from {ontology_path}")
        self.graph.parse(ontology_path, format="xml")

        print(f"Loading data from {data_path}")
        self.graph.parse(data_path, format="turtle")

        # Define namespaces
        self.elib = Namespace("http://www.semanticweb.org/e-library#")
        self.graph.bind("elib", self.elib)

        print(f"Graph loaded with {len(self.graph)} triples")

    def search_by_title(self, keyword):
        """Search resources by title keyword."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?resource ?title ?type
        WHERE {
          ?resource elib:title ?title .
          ?resource rdf:type ?type .
          FILTER(CONTAINS(LCASE(?title), LCASE(?keyword)))
          FILTER(?type != owl:NamedIndividual)
        }
        """
        results = self.graph.query(query, initBindings={"keyword": Literal(keyword)})
        return list(results)

    def search_by_author(self, author_name):
        """Search resources by author name."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?resource ?title ?authorName
        WHERE {
          ?resource elib:title ?title .
          ?resource elib:hasAuthor ?author .
          ?author elib:name ?authorName .
          FILTER(CONTAINS(LCASE(?authorName), LCASE(?author_name)))
        }
        """
        results = self.graph.query(
            query, initBindings={"author_name": Literal(author_name)}
        )
        return list(results)

    def search_by_subject(self, subject_name):
        """Search resources by subject."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?resource ?title ?subjectName
        WHERE {
          ?resource elib:title ?title .
          ?resource elib:hasTopic ?subject .
          ?subject elib:subjectName ?subjectName .
          FILTER(CONTAINS(LCASE(?subjectName), LCASE(?subject_name)))
        }
        """
        results = self.graph.query(
            query, initBindings={"subject_name": Literal(subject_name)}
        )
        return list(results)

    def search_by_date_range(self, start_date, end_date):
        """Search resources by publication date range."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?resource ?title ?date
        WHERE {
          ?resource elib:title ?title .
          ?resource elib:publicationDate ?date .
          FILTER(?date >= ?start_date && ?date <= ?end_date)
        }
        ORDER BY DESC(?date)
        """
        results = self.graph.query(
            query,
            initBindings={
                "start_date": Literal(start_date, datatype=XSD.date),
                "end_date": Literal(end_date, datatype=XSD.date),
            },
        )
        return list(results)

    def find_related_resources(self, resource_uri):
        """Find resources related to a specific resource."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>

        SELECT ?relatedResource ?relatedTitle
        WHERE {
          ?resource elib:relatedTo ?relatedResource .
          ?relatedResource elib:title ?relatedTitle .
        }
        """
        resource = URIRef(resource_uri)
        results = self.graph.query(query, initBindings={"resource": resource})
        return list(results)

    def find_citing_resources(self, resource_uri):
        """Find resources that cite a specific resource."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>

        SELECT ?citingResource ?citingTitle
        WHERE {
          ?citingResource elib:cites ?resource .
          ?citingResource elib:title ?citingTitle .
        }
        """
        resource = URIRef(resource_uri)
        results = self.graph.query(query, initBindings={"resource": resource})
        return list(results)

    def find_resources_by_topic_hierarchy(self, topic_class):
        """Find resources by topic hierarchy (resources on a topic and its subtopics)."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?resource ?title ?topicName
        WHERE {
          ?resource elib:title ?title .
          ?resource elib:hasTopic ?topic .
          ?topic elib:subjectName ?topicName .
          {
            ?topic rdf:type ?topic_class .
          } UNION {
            ?subTopic rdfs:subClassOf ?topic_class .
            ?topic rdf:type ?subTopic .
          }
        }
        """
        topic = URIRef(topic_class)
        results = self.graph.query(query, initBindings={"topic_class": topic})
        return list(results)

    def find_interdisciplinary_resources(self):
        """Find resources with multiple topics (interdisciplinary)."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>

        SELECT ?resource ?title ?topic1Name ?topic2Name
        WHERE {
          ?resource elib:title ?title .
          ?resource elib:hasTopic ?topic1 .
          ?resource elib:hasTopic ?topic2 .
          ?topic1 elib:subjectName ?topic1Name .
          ?topic2 elib:subjectName ?topic2Name .
          FILTER(?topic1 != ?topic2)
        }
        """
        results = self.graph.query(query)
        return list(results)

    def find_collaborating_authors(self):
        """Find authors who have collaborated."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>

        SELECT DISTINCT ?author1Name ?author2Name ?resourceTitle
        WHERE {
          ?resource elib:hasAuthor ?author1 .
          ?resource elib:hasAuthor ?author2 .
          ?resource elib:title ?resourceTitle .
          ?author1 elib:name ?author1Name .
          ?author2 elib:name ?author2Name .
          FILTER(?author1 != ?author2 && ?author1Name < ?author2Name)
        }
        """
        results = self.graph.query(query)
        return list(results)

    def find_all_academic_resources(self):
        """Find all academic resources (including inferred subclasses)."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?resource ?title ?type
        WHERE {
          ?resource rdf:type ?type .
          ?type rdfs:subClassOf* elib:AcademicResource .
          ?resource elib:title ?title .
        }
        """
        results = self.graph.query(query)
        return list(results)

    def find_most_cited_resources(self):
        """Find the most cited resources."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>

        SELECT ?resource ?title (COUNT(?citing) as ?citationCount)
        WHERE {
          ?citing elib:cites ?resource .
          ?resource elib:title ?title .
        }
        GROUP BY ?resource ?title
        ORDER BY DESC(?citationCount)
        """
        results = self.graph.query(query)
        return list(results)

    def search_by_keyword_in_title_or_abstract(self, keyword):
        """Find resources by keyword in title or abstract."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>

        SELECT ?resource ?title ?abstract
        WHERE {
          ?resource elib:title ?title .
          ?resource elib:abstract ?abstract .
          FILTER(CONTAINS(LCASE(?title), LCASE(?keyword)) || CONTAINS(LCASE(?abstract), LCASE(?keyword)))
        }
        """
        results = self.graph.query(query, initBindings={"keyword": Literal(keyword)})
        return list(results)

    def recommend_similar_resources(self, resource_uri):
        """Recommendation query - find similar resources based on shared topics."""
        query = """
        PREFIX elib: <http://www.semanticweb.org/e-library#>

        SELECT ?recommendedResource ?recommendedTitle (COUNT(?sharedTopic) as ?relevance)
        WHERE {
          ?resource elib:hasTopic ?topic .
          ?recommendedResource elib:hasTopic ?topic .
          ?recommendedResource elib:title ?recommendedTitle .
          FILTER(?recommendedResource != ?resource)
          BIND(?topic as ?sharedTopic)
        }
        GROUP BY ?recommendedResource ?recommendedTitle
        ORDER BY DESC(?relevance)
        """
        resource = URIRef(resource_uri)
        results = self.graph.query(query, initBindings={"resource": resource})
        return list(results)

    def execute_custom_query(self, query_string):
        """Execute a custom SPARQL query."""
        results = self.graph.query(query_string)
        return list(results)


# Example usage
if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)

    # Paths to ontology and data files
    ontology_path = os.path.join(project_dir, "ontology", "e-library.owl")
    data_path = os.path.join(project_dir, "data", "sample_data.ttl")

    # Initialize the search engine
    search_engine = ELibrarySemanticSearch(ontology_path, data_path)
