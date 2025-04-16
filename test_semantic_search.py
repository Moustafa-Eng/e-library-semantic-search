import os
import sys
import unittest
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

from src.semantic_search import ELibrarySemanticSearch

class TestELibrarySemanticSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment once before all tests."""
        # Paths to ontology and data files
        ontology_path = os.path.join(project_dir, "ontology", "e-library.owl")
        data_path = os.path.join(project_dir, "data", "sample_data.ttl")
        
        # Initialize the search engine
        cls.search_engine = ELibrarySemanticSearch(ontology_path, data_path)
        
        print(f"Test setup complete. Graph loaded with {len(cls.search_engine.graph)} triples")
    
    def test_ontology_consistency(self):
        """Test that the ontology is consistent."""
        # Check if the ontology has expected classes
        expected_classes = [
            "AcademicResource", "Book", "Journal", "Article", "Thesis", 
            "ConferencePaper", "Person", "Subject", "Organization"
        ]
        
        for class_name in expected_classes:
            class_uri = URIRef(f"http://www.semanticweb.org/e-library#{class_name}")
            self.assertTrue(
                (class_uri, RDF.type, OWL.Class) in self.search_engine.graph,
                f"Class {class_name} not found in ontology"
            )
        
        # Check if the ontology has expected object properties
        expected_obj_props = [
            "hasAuthor", "publishedBy", "hasTopic", "cites", "relatedTo"
        ]
        
        for prop_name in expected_obj_props:
            prop_uri = URIRef(f"http://www.semanticweb.org/e-library#{prop_name}")
            self.assertTrue(
                (prop_uri, RDF.type, OWL.ObjectProperty) in self.search_engine.graph,
                f"Object property {prop_name} not found in ontology"
            )
        
        # Check if the ontology has expected data properties
        expected_data_props = [
            "title", "abstract", "publicationDate", "isbn", "keywords"
        ]
        
        for prop_name in expected_data_props:
            prop_uri = URIRef(f"http://www.semanticweb.org/e-library#{prop_name}")
            self.assertTrue(
                (prop_uri, RDF.type, OWL.DatatypeProperty) in self.search_engine.graph,
                f"Data property {prop_name} not found in ontology"
            )
    
    def test_search_by_title(self):
        """Test searching resources by title keyword."""
        results = self.search_engine.search_by_title("semantic")
        self.assertTrue(len(results) > 0, "No results found for title search")
        
        # Check if all results contain the keyword in title
        for row in results:
            self.assertTrue(
                "semantic" in str(row.title).lower(),
                f"Result title '{row.title}' does not contain 'semantic'"
            )
    
    def test_search_by_author(self):
        """Test searching resources by author name."""
        results = self.search_engine.search_by_author("Smith")
        self.assertTrue(len(results) > 0, "No results found for author search")
        
        # Check if all results have the author
        for row in results:
            self.assertTrue(
                "smith" in str(row.authorName).lower(),
                f"Result author '{row.authorName}' is not 'Smith'"
            )
    
    def test_search_by_subject(self):
        """Test searching resources by subject."""
        results = self.search_engine.search_by_subject("Semantic Web")
        self.assertTrue(len(results) > 0, "No results found for subject search")
        
        # Check if all results have the subject
        for row in results:
            self.assertTrue(
                "semantic web" in str(row.subjectName).lower(),
                f"Result subject '{row.subjectName}' is not 'Semantic Web'"
            )
    
    def test_search_by_date_range(self):
        """Test searching resources by publication date range."""
        results = self.search_engine.search_by_date_range("2022-01-01", "2023-12-31")
        self.assertTrue(len(results) > 0, "No results found for date range search")
        
        # Check if all results are within the date range
        for row in results:
            date_str = str(row.date)
            self.assertTrue(
                "2022-01-01" <= date_str <= "2023-12-31",
                f"Result date '{date_str}' is not within range"
            )
    
    def test_find_related_resources(self):
        """Test finding resources related to a specific resource."""
        resource_uri = "http://www.semanticweb.org/e-library#article1"
        results = self.search_engine.find_related_resources(resource_uri)
        self.assertTrue(len(results) > 0, "No related resources found")
    
    def test_find_citing_resources(self):
        """Test finding resources that cite a specific resource."""
        resource_uri = "http://www.semanticweb.org/e-library#book1"
        results = self.search_engine.find_citing_resources(resource_uri)
        self.assertTrue(len(results) > 0, "No citing resources found")
    
    def test_find_interdisciplinary_resources(self):
        """Test finding resources with multiple topics (interdisciplinary)."""
        results = self.search_engine.find_interdisciplinary_resources()
        self.assertTrue(len(results) > 0, "No interdisciplinary resources found")
    
    def test_find_collaborating_authors(self):
        """Test finding authors who have collaborated."""
        results = self.search_engine.find_collaborating_authors()
        self.assertTrue(len(results) > 0, "No collaborating authors found")
    
    def test_find_all_academic_resources(self):
        """Test finding all academic resources (including inferred subclasses)."""
        results = self.search_engine.find_all_academic_resources()
        self.assertTrue(len(results) > 0, "No academic resources found")
    
    def test_find_most_cited_resources(self):
        """Test finding the most cited resources."""
        results = self.search_engine.find_most_cited_resources()
        self.assertTrue(len(results) > 0, "No cited resources found")
    
    def test_search_by_keyword_in_title_or_abstract(self):
        """Test finding resources by keyword in title or abstract."""
        results = self.search_engine.search_by_keyword_in_title_or_abstract("semantic")
        self.assertTrue(len(results) > 0, "No results found for keyword search")
        
        # Check if all results contain the keyword in title or abstract
        for row in results:
            self.assertTrue(
                "semantic" in str(row.title).lower() or "semantic" in str(row.abstract).lower(),
                f"Result does not contain 'semantic' in title or abstract"
            )
    
    def test_recommend_similar_resources(self):
        """Test recommendation query - find similar resources based on shared topics."""
        resource_uri = "http://www.semanticweb.org/e-library#article1"
        results = self.search_engine.recommend_similar_resources(resource_uri)
        self.assertTrue(len(results) > 0, "No similar resources found")

if __name__ == '__main__':
    unittest.main()
