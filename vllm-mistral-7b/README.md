# mistral-7b inference testing

### testing via curl (now using OpenAI API)

```
kubectl -n vllm port-forward service/vllm-openai 8000:8000

curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "mistralai/Mistral-7B-Instruct-v0.3",
        "prompt": "Where is Chicago?",
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.2
    }'


curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" -s \
  -d '{
  "model": "mistralai/Mistral-7B-Instruct-v0.3",
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
  -H "Content-Type: application/json" -s \
  -d '{
  "model": "mistralai/Mistral-7B-Instruct-v0.3",
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
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
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
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "prompt": "San Francisco is a",
    "max_tokens": 100,
    "temperature": 0
}'

curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "mistralai/Mistral-7B-Instruct-v0.3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'

```