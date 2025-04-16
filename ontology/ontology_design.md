# E-Library Ontology Design

This document outlines the detailed class hierarchy, properties, and relationships for the E-Library ontology.

## Class Hierarchy

```
owl:Thing
  ├── AcademicResource
  │     ├── Book
  │     ├── Journal
  │     ├── Article
  │     │     ├── JournalArticle
  │     │     └── ConferenceArticle
  │     ├── Thesis
  │     │     ├── MastersThesis
  │     │     └── DoctoralThesis
  │     ├── ConferencePaper
  │     └── TechnicalReport
  ├── Person
  │     ├── Author
  │     ├── Editor
  │     └── Researcher
  ├── Organization
  │     ├── Publisher
  │     ├── University
  │     └── ResearchInstitution
  ├── Subject
  │     ├── ComputerScience
  │     ├── Mathematics
  │     ├── Physics
  │     ├── Biology
  │     ├── Chemistry
  │     ├── Engineering
  │     ├── SocialSciences
  │     └── Humanities
  └── Event
        └── Conference
```

## Object Properties

- **hasAuthor**: Domain: AcademicResource, Range: Person
- **hasEditor**: Domain: AcademicResource, Range: Person
- **publishedBy**: Domain: AcademicResource, Range: Publisher
- **hasTopic**: Domain: AcademicResource, Range: Subject
- **cites**: Domain: AcademicResource, Range: AcademicResource
- **relatedTo**: Domain: AcademicResource, Range: AcademicResource
- **affiliatedWith**: Domain: Person, Range: Organization
- **partOf**: Domain: JournalArticle, Range: Journal
- **presentedAt**: Domain: ConferencePaper, Range: Conference
- **supervisedBy**: Domain: Thesis, Range: Person

## Data Properties

- **title**: Domain: AcademicResource, Range: xsd:string
- **abstract**: Domain: AcademicResource, Range: xsd:string
- **publicationDate**: Domain: AcademicResource, Range: xsd:date
- **keywords**: Domain: AcademicResource, Range: xsd:string
- **isbn**: Domain: Book, Range: xsd:string
- **issn**: Domain: Journal, Range: xsd:string
- **doi**: Domain: AcademicResource, Range: xsd:string
- **pageCount**: Domain: AcademicResource, Range: xsd:integer
- **language**: Domain: AcademicResource, Range: xsd:string
- **name**: Domain: Person, Range: xsd:string
- **email**: Domain: Person, Range: xsd:string
- **organizationName**: Domain: Organization, Range: xsd:string
- **subjectName**: Domain: Subject, Range: xsd:string
- **subjectDescription**: Domain: Subject, Range: xsd:string

## Restrictions and Axioms

- Every Book must have at least one Author
- Every JournalArticle must be part of exactly one Journal
- Every Thesis must have exactly one supervisor
- Every AcademicResource must have at least one Subject
- ConferenceArticle and ConferencePaper must be presented at exactly one Conference

## Annotations

- rdfs:label - Human-readable labels for all classes and properties
- rdfs:comment - Descriptive comments for classes and properties
- dc:creator - Creator information for the ontology
- dc:description - Description of the ontology purpose
