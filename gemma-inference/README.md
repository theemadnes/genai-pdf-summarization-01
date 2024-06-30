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

### testing via curl

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