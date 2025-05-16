model=ipipan/silver-retriever-base-v1
volume=$PWD/embedding_model/data # share a volume with the Docker container to avoid downloading weights every run

docker run -p 8085:80 -v $volume:/data --pull always ghcr.io/huggingface/text-embeddings-inference:cpu-1.6 --model-id $model