from openai import OpenAI
from pathlib import Path  
import weaviate.classes.config as wc 
import weaviate
CLIENT = OpenAI(base_url='http://localhost:8085/v1', api_key='SAN_EDU')


COLLECTION_NAME = 'wiesiek_b2'



def calculate_embedding(text):
    response = CLIENT.embeddings.create(input='</s>' + text, model='ipipan/silver-retriever-base-v1')
    embedding = response.data[0].embedding
    return embedding

def load_data(data_path):
    texts = []
    for fil in Path(data_path).glob('*.txt'):
        texts.append(fil.read_text(encoding='utf-8'))

    return texts

def chunk_text(text ,chunk_size, chunk_overlap):
    result = []

    for i in range(0, len(text), chunk_size - chunk_overlap):
        text_chunk = text [i : i + chunk_size]
        result.append(text_chunk)

    return result

def main():

    texts = load_data('./dane')

    text_chunks = []

    for text in texts:
        text_chunk_part = chunk_text(text, chunk_size=512, chunk_overlap=128)
        text_chunks.extend(text_chunk_part)

    embeddings = []
    for text_chunk in text_chunks:
        embedding = calculate_embedding(text_chunk)
        embeddings.append(embedding)

    print(len(embeddings), len(embeddings[0]))

    DB_CLIENT = weaviate.connect_to_local(host='localhost', port=8080, grpc_port=50051)

    
    DB_CLIENT.collections.create(
        COLLECTION_NAME,
        properties=[
            wc.Property(name="text", data_type=wc.DataType.TEXT),
        ],  
        vector_index_config=wc.Configure.VectorIndex.hnsw(
            distance_metric=wc.VectorDistances.COSINE
        )
    )

    collection = DB_CLIENT.collections.get(COLLECTION_NAME)

    for text_chank, embedding in zip(text_chunks, embeddings):
        collection.data.insert(
            properties={
                "text": text_chank,
            },
            vector=embedding,
        )



    total_count = collection.aggregate.over_all(total_count=True).total_count
    print(total_count)


    DB_CLIENT.close()


if __name__ == "__main__":
    main()

# print(calculate_embedding("SAN to najlepsza uczelia"))