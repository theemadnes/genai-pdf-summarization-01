# gemma inference testing

### basic setup

```
# using GKE autopilot and namespace `vllm`
# make sure to export HF_TOKEN=hf_api_token

kubectl apply -f 0_namespace.yaml 

kubectl create secret generic hf-secret \
-n vllm \
--from-literal=hf_api_token=$HF_TOKEN \
--dry-run=client -o yaml | kubectl apply -f -

kubectl apply -f vllm-2b.yaml

# wait for the deployment to be ready
kubectl -n vllm wait --for=condition=Available --timeout=700s deployment/vllm-gemma-deployment
```


### testing via curl (now using OpenAI API)

```
kubectl -n vllm port-forward service/vllm-openai 8000:8000

curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "google/gemma-2-2b-it",
        "prompt": "Where is Chicago?",
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.2
    }'


curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" -s \
  -d '{
  "model": "google/gemma-2-2b-it",
  "messages": [
    {
      "role": "user",
      "content": "Where is Chicago?"
    }
  ],
  "temperature": 0.2,
  "top_k": 1.0,
  "top_p": 0.2,
  "max_tokens": 512
}' \
| jq -r '.choices[0].message.content'

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
  "model": "google/gemma-2-2b-it",
  "messages": [
    {
      "role": "user",
      "content": "Tell me about Chicago"
    }
  ],
  "temperature": 0.5,
  "top_k": 1.0,
  "top_p": 1.0,
  "max_tokens": 512
}' \
| jq -r '.choices[0].message.content'

curl http://localhost:8000/v1/chat/completions   -H "Content-Type: application/json" -d '{
    "model": "google/gemma-2-2b",
    "messages": [
      {
        "role": "system",
        "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."
      },
      {
        "role": "user",
        "content": "Compose a poem that explains the concept of recursion in programming."
      }
    ]
  }'

curl http://localhost:8000/v1/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "google/gemma-2-2b-it",
    "prompt": "San Francisco is a",
    "max_tokens": 100,
    "temperature": 0
}'

curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "google/gemma-2-2b-it",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'

```


### (OLD) testing via curl

```
kubectl -n vllm port-forward service/llm-service 8000:8000

USER_PROMPT="Java is a"

curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
    "prompt": "${USER_PROMPT}",
    "temperature": 0.90,
    "top_p": 1.0,
    "max_tokens": 4096
}
EOF
```