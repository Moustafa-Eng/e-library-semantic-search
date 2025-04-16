import os
import sys
from flask import Flask, render_template, request, jsonify
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

from src.semantic_search import ELibrarySemanticSearch

app = Flask(__name__)

# Initialize the search engine
ontology_path = "D:\Semester_8\Semantic Web\e-library-semantic-search\ontology\e-library.owl"
data_path = "D:\Semester_8\Semantic Web\e-library-semantic-search\data\sample_data.ttl"
search_engine = ELibrarySemanticSearch(ontology_path, data_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form.get('search_type')
    query = request.form.get('query')
    results = []
    
    if search_type == 'title':
        results = search_engine.search_by_title(query)
        formatted_results = [
            {
                'resource': str(row.resource),
                'title': str(row.title),
                'type': str(row.type).split('#')[-1]
            }
            for row in results
        ]
    elif search_type == 'author':
        results = search_engine.search_by_author(query)
        formatted_results = [
            {
                'resource': str(row.resource),
                'title': str(row.title),
                'author': str(row.authorName)
            }
            for row in results
        ]
    elif search_type == 'subject':
        results = search_engine.search_by_subject(query)
        formatted_results = [
            {
                'resource': str(row.resource),
                'title': str(row.title),
                'subject': str(row.subjectName)
            }
            for row in results
        ]
    elif search_type == 'keyword':
        results = search_engine.search_by_keyword_in_title_or_abstract(query)
        formatted_results = [
            {
                'resource': str(row.resource),
                'title': str(row.title),
                'abstract': str(row.abstract)
            }
            for row in results
        ]
    elif search_type == 'date_range':
        # Assuming query is in format "YYYY-MM-DD,YYYY-MM-DD"
        start_date, end_date = query.split(',')
        results = search_engine.search_by_date_range(start_date, end_date)
        formatted_results = [
            {
                'resource': str(row.resource),
                'title': str(row.title),
                'date': str(row.date)
            }
            for row in results
        ]
    elif search_type == 'interdisciplinary':
        results = search_engine.find_interdisciplinary_resources()
        formatted_results = [
            {
                'resource': str(row.resource),
                'title': str(row.title),
                'topic1': str(row.topic1Name),
                'topic2': str(row.topic2Name)
            }
            for row in results
        ]
    elif search_type == 'most_cited':
        results = search_engine.find_most_cited_resources()
        formatted_results = [
            {
                'resource': str(row.resource),
                'title': str(row.title),
                'citations': str(row.citationCount)
            }
            for row in results
        ]
    elif search_type == 'collaborating_authors':
        results = search_engine.find_collaborating_authors()
        formatted_results = [
            {
                'author1': str(row.author1Name),
                'author2': str(row.author2Name),
                'resource': str(row.resourceTitle)
            }
            for row in results
        ]
    else:
        formatted_results = []
    
    return jsonify(formatted_results)

@app.route('/recommend/<resource_id>')
def recommend(resource_id):
    resource_uri = f"http://www.semanticweb.org/e-library#{resource_id}"
    results = search_engine.recommend_similar_resources(resource_uri)
    formatted_results = [
        {
            'resource': str(row.recommendedResource),
            'title': str(row.recommendedTitle),
            'relevance': str(row.relevance)
        }
        for row in results
    ]
    return jsonify(formatted_results)

@app.route('/related/<resource_id>')
def related(resource_id):
    resource_uri = f"http://www.semanticweb.org/e-library#{resource_id}"
    results = search_engine.find_related_resources(resource_uri)
    formatted_results = [
        {
            'resource': str(row.relatedResource),
            'title': str(row.relatedTitle)
        }
        for row in results
    ]
    return jsonify(formatted_results)

@app.route('/citing/<resource_id>')
def citing(resource_id):
    resource_uri = f"http://www.semanticweb.org/e-library#{resource_id}"
    results = search_engine.find_citing_resources(resource_uri)
    formatted_results = [
        {
            'resource': str(row.citingResource),
            'title': str(row.citingTitle)
        }
        for row in results
    ]
    return jsonify(formatted_results)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(project_dir, "src", "templates")
    os.makedirs(templates_dir, exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
