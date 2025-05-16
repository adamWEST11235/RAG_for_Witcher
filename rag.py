import ollama
from data_to_db_emb import calculate_embedding, COLLECTION_NAME
import weaviate
from weaviate.classes.query import MetadataQuery

def generate_answer(query):
    messages = [
        {"role": "system", "content": "Jesteś asystentem wiedzmina pomagasz my w szukaniu informacji na temat potworów."},
        {"role": "user", "content": f"Context: {query}?"}
    ]

    response = ollama.chat(model='llama3.2:latest', messages=messages)
    # print(response['message']['content'])
    return response.message.content

def prepare_prompt_with_context(question, documents):
    prompt = f"""
    Odpowiedz na pytanie używając poniższych dokumentów:
    Pytanie: {question}
    """
    for idx, document in enumerate(documents):
        prompt += '\n' + f'<document {idx +1 }>' + document + f'</document {idx + 1}>'

    return prompt    


question = 'Jak walczyć z żywiołakiem ognia?'

embedding = calculate_embedding(f'Pytanie: {question}')
print(embedding)
# print(embedding)

DB_CLIENT = weaviate.connect_to_local(host='localhost', port=8080, grpc_port=50051)
collection = DB_CLIENT.collections.get(COLLECTION_NAME)
response = collection.query.near_vector(
    near_vector=embedding,
    limit=4,
    return_metadata=MetadataQuery(distance=True)
)

# print(response)


text_documents = []
for doc in response.objects:
    print(doc.properties)
    # print(doc.metadata.distance)
    text_documents.append(doc.properties['text'])

fresh_ans = generate_answer(question)



print("Odp bez rag--------------")
print(fresh_ans)
print()

prompt = prepare_prompt_with_context(question=question, documents=text_documents)
print()
print(prompt)
print()


ans = generate_answer(prompt)
print()
print("Odp z rag--------------")
print(ans)
DB_CLIENT.close()
# generate_answer()