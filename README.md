# Search Engine Web Crawler with Advanced Retrieval Models

## Overview

This project is a Python-based search engine web crawler that integrates advanced information retrieval models, including BM25, TF-IDF, and language models (LM) for document retrieval and ranking. It leverages Elasticsearch for indexing and querying, and utilizes pseudo-relevance feedback to enhance search results. Additionally, it features training and testing phases for different models and explores various smoothing techniques.

## Key Components

### 1. Web Crawling and Data Parsing
- **`data_parser.py`**: A script that handles the extraction and parsing of data from crawled web pages. It processes HTML content, removes stop words, and prepares the data for indexing.
- **`parser.py`**: Another parsing utility that might be focused on handling different data formats or additional preprocessing steps.

### 2. Indexing and Retrieval with Elasticsearch
- **`es.py`**: The main script for interacting with Elasticsearch, setting up connections, and handling basic indexing and querying operations.
- **`es_index_data.py`**: Responsible for indexing parsed documents into Elasticsearch. It structures the data into a format suitable for Elasticsearch indexing.
- **`es_retreival_models.py`**: Implements various retrieval models on top of Elasticsearch, such as BM25 and TF-IDF. It customizes Elasticsearch queries to apply these models and retrieves ranked lists of documents.

### 3. Information Retrieval Models
- **BM25**:
  - **`bm25_result.txt`**: Stores the results of the BM25 retrieval model.
  - **`bm25_pseudo_rel_result.txt`** and **`bm25_pseudo_rel_result_es.txt`**: Results incorporating pseudo-relevance feedback to improve retrieval effectiveness.
- **Language Models (LM)**:
  - **`lmjm_result.txt`**: Results from a language model with Jelinek-Mercer smoothing.
  - **`lml_result.txt`**: Results from another variation of a language model.
- **TF-IDF**:
  - **`tfidf_result.txt`**: Results from the TF-IDF retrieval model.
- **Okapi TF**:
  - **`okapitf_result.txt`**: Stores results using the Okapi TF retrieval model.
  
### 4. Pseudo-Relevance Feedback
- **`pseudo_rel_feedback.py`**: A script implementing pseudo-relevance feedback, which refines search results based on an initial round of retrieval.
- **`pseudo_rel_es.py`**: Applies pseudo-relevance feedback directly within Elasticsearch.

### 5. Evaluation and Testing
- **`qrels.adhoc.51-100.AP89.txt`**: A file containing relevance judgments, used to evaluate the performance of the retrieval models.
- **`query_desc.51-100.short.txt`**: A set of queries used to test the retrieval models.
- **`results.xlsx`**: A spreadsheet containing detailed results and comparisons across different models and experiments.

### 6. Additional Scripts and Utilities
- **`main.py`**: Likely the main entry point for running the project, coordinating the crawling, indexing, and retrieval processes.
- **`stemming_ind.py`**: Handles stemming of words in the documents, possibly using a predefined list of stemming rules (`stem-classes.lst`).
- **`stoplist.txt`**: A list of stop words to be removed during the parsing process.
- **`term_vectors.json`**: A JSON file that might store term vectors for documents, aiding in retrieval and ranking.

## How It Works

1. **Crawling and Parsing**: The project starts by crawling the web (if integrated with a crawler) and parsing the HTML content to extract relevant text data.
2. **Indexing**: Parsed data is indexed into Elasticsearch, where it is stored in a structured format suitable for retrieval.
3. **Retrieval Models**: Various retrieval models, including BM25, TF-IDF, and language models, are applied to the indexed data to retrieve and rank documents based on relevance to user queries.
4. **Pseudo-Relevance Feedback**: An initial round of retrieval is refined using pseudo-relevance feedback, improving the ranking of relevant documents.
5. **Evaluation**: The effectiveness of different models is evaluated using standard relevance judgments, and results are stored for comparison.

## Prerequisites

- **Python 3.x**
- **Elasticsearch**
- **Kibana** (optional, for visualization)
- **Python Libraries**: `elasticsearch`, `requests`, `BeautifulSoup`, `pandas`, `numpy`, `nltk`

## Installation

1. **Install Elasticsearch and Kibana**:
   - Follow the official Elasticsearch and Kibana installation guides.
   
2. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Search-Engine-Web-Crawler
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Elasticsearch**:
   - Ensure Elasticsearch is running and update the connection settings in `es.py` or other relevant scripts.

## Running the Project

1. **Index Data**:
   - Use `es_index_data.py` to index the parsed data into Elasticsearch.
   ```bash
   python es_index_data.py
   ```

2. **Run Retrieval Models**:
   - Execute `es_retreival_models.py` or other relevant scripts to perform document retrieval.
   ```bash
   python es_retreival_models.py
   ```

3. **Evaluate Results**:
   - Compare the results stored in `.txt` files or `results.xlsx` to evaluate the effectiveness of different retrieval models.

## Conclusion

This project provides a comprehensive implementation of a search engine using Python, Elasticsearch, and advanced retrieval models. It demonstrates the power of combining traditional IR models with modern search technologies and offers a robust framework for further experimentation and development.