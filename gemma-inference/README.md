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