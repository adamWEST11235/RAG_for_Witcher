# System RAG z Weaviate i Ollama

Ten projekt implementuje system Retrieval-Augmented Generation (RAG) wykorzystujący Weaviate jako bazę danych wektorową i Ollama do inferencji modelu językowego.


## Wymagania

- Python 3.8+
- Weaviate uruchomiony lokalnie (port 8080)
- Ollama zainstalowana i uruchomiona
- Lokalny serwer modelu embeddingowego (port 8085)

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/adamWEST11235/RAG_for_Witcher.git
```

2. Utwórz i aktywuj środowisko wirtualne:
```bash
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate
```

3. Zainstaluj zależności:
```bash

pip install -r requirements.txt

## Użycie

1. Uruchom serwer modelu embeddingowego:
```bash
./run_embedding_model.sh
```

2. Uruchom Weaviate:
```bash
./run_vector_db.sh
```

3. Przetwórz i wygeneruj embeddingi:
```bash
python data_to_db_emb.py
```

4. Uruchom zapytania RAG:
```bash
python rag.py
```

## Konfiguracja

- System wykorzystuje model `ipipan/silver-retriever-base-v1` do generowania embeddingów
- Weaviate jest skonfigurowany do działania na localhost:8080
- Ollama wykorzystuje model `llama3.2:latest`

## Licencja

MIT License
