
# This script starts a Kubernetes cluster using Minikube,
# verifies that the cluster is running,
# and retrieves the available pods.

# Start Minikube Cluster
minikube start

# Check if Minikube started successfully
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start Minikube. Please check Docker or your virtualization settings."
    exit 1
}

# Verify Cluster Info
kubectl cluster-info

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ kubectl could not connect to the cluster. Check that Minikube is running."
    exit 1
}

# Retrieve Available Pods
kubectl get pods -A

Write-Host "Kubernetes cluster is up and running!"
