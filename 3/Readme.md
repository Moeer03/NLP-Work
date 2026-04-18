"""
README - NLP Desktop Search Engine
Lab Assignment: Building a Full-Text Search Engine
"""

## Project Overview

This is a complete implementation of a **Desktop Search Engine** for indexing and searching multiple document types (TXT, DOCX, PDF).

### Features Implemented

1. **Multi-Format Document Processing**
   - Extract text from `.txt`, `.docx`, and `.pdf` files
   - Handles all 20 documents in the data folder
   - Graceful error handling for missing libraries

2. **Text Preprocessing & NLP**
   - Text cleaning (lowercase, remove special chars, URLs, emails)
   - Tokenization using NLTK if available, else basic splitting
   - Stopword removal (English stopwords)
   - Porter Stemming for term normalization
   - Optional lemmatization support

3. **Inverted Index Building**
   - Creates term-to-document mapping
   - Calculates TF (Term Frequency) scores
   - Computes IDF (Inverse Document Frequency) values
   - Generates TF-IDF scores for ranking

4. **Multiple Search Types**
   - **TF-IDF Search**: Relevance-based ranking using term importance
   - **Vector Space Model**: Cosine similarity between query and documents
   - **Boolean Search**: 
     - AND operator: documents must contain ALL terms
     - OR operator: documents containing ANY term
     - NOT operator: exclude documents with certain terms

5. **Index Persistence**
   - Saves built index to disk (`index/` folder)
   - Loads pre-built index for faster searches
   - Stores metadata (document info, term frequencies, IDF values)

### Project Structure

```
project/
├── data/
│   ├── doc_01.txt to doc_10.txt (10 text documents)
│   ├── doc_01.docx to doc_05.docx (5 Word documents)
│   └── doc_01.pdf to doc_05.pdf (5 PDF documents)
├── index/
│   ├── inverted_index.json (term -> document mapping)
│   └── metadata.json (document info, IDF values)
└── src/
    ├── document_processor.py (Load documents from all formats)
    ├── text_preprocessor.py (NLP text processing pipeline)
    ├── search_index.py (Build and manage inverted index)
    ├── search_engine.py (Perform various searches)
    └── main.py (Interactive CLI interface)
```

### Core Modules

#### 1. DocumentProcessor (`document_processor.py`)
- Loads documents from data directory
- Supports TXT, DOCX, PDF file formats
- Returns dictionary of {doc_id: (filename, content)}

#### 2. TextPreprocessor (`text_preprocessor.py`)
- Cleans raw text (remove URLs, special chars)
- Tokenizes text into words
- Removes stopwords (the, a, an, etc.)
- Applies stemming using Porter Stemmer
- Provides term frequency analysis

#### 3. SearchIndex (`search_index.py`)
- Builds inverted index from tokenized documents
- Calculates TF-IDF scores
- Persists index to JSON files
- Retrieves documents by term
- Provides index statistics

#### 4. SearchEngine (`search_engine.py`)
- Performs TF-IDF ranking search
- Implements Boolean operators (AND, OR, NOT)
- Implements Vector Space Model with cosine similarity
- Returns ranked list of relevant documents

#### 5. Main Application (`main.py`)
- Interactive command-line interface
- Commands supported:
  - Simple search: `machine learning`
  - Boolean AND: `deep AND learning`
  - Boolean OR: `python OR java`
  - Boolean NOT: `search NOT data`
  - Special commands: `stats`, `rebuild`, `help`, `quit`

### Installation & Usage

```bash
# Install dependencies
pip install nltk python-docx pdfplumber reportlab tqdm

# Navigate to project directory
cd "d:\Data Science\Semester VI\BS DS Morning Sem VI\Data Science Semester VI\NLP\Assignments\3"

# Run the search engine
python src/main.py
```

### Example Searches

```
Search > machine learning
Results:
1. [01] doc_01.txt (Score: 5.2341)
2. [03] doc_03.txt (Score: 3.1245)
...

Search > deep AND learning
Results:
1. [03] doc_03.txt
2. [01] doc_01.txt
...

Search > stats
Index Statistics:
- Total Documents: 20
- Unique Terms: 2547
- Average Document Length: 125.3 terms
```

### Index Statistics

After building the index on all 20 documents:
- **Total Documents**: 20 files (10 TXT, 5 DOCX, 5 PDF)
- **Unique Terms**: ~2500+ after preprocessing
- **Average Doc Length**: ~120-150 tokens per document
- **TF-IDF Computation**: Automatic ranking of documents by relevance

### NLP Techniques Used

1. **Text Normalization**: Lowercase conversion, punctuation removal
2. **Tokenization**: Word-level splitting with NLTK
3. **Stopword Filtering**: Remove common English words
4. **Stemming**: Porter Stemmer for word root extraction
5. **TF-IDF**: Classic information retrieval scoring
6. **Vector Space Model**: Cosine similarity for ranking
7. **Boolean Retrieval**: Set operations for structured queries
8. **Inverted Index**: Efficient term-to-document mapping

### Deliverables

✅ 20 sample documents (10 TXT, 5 DOCX, 5 PDF) with real NLP content
✅ Full-text search index with TF-IDF scoring
✅ Multiple search algorithms (TF-IDF, Vector Space, Boolean)
✅ Interactive command-line interface
✅ Persistent index storage and loading
✅ Comprehensive NLP text preprocessing
✅ Document metadata and statistics
✅ Main application with CLI

### Author
NLP Assignment - Desktop Search Engine Implementation
Date: March 8, 2026
