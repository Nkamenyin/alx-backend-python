# kurbeScript.ps1
# Author: Valentine Eyet
# Description: Starts a Kubernetes cluster using Minikube,
# verifies it’s running, and retrieves available pods.



# Start Minikube cluster

Write-Host "Starting Minikube cluster..."
try {
    minikube start --driver=docker
} catch {
    Write-Host "Minikube failed to start with Docker driver. Trying default driver..."
    minikube start
}


# Verify cluster status

Write-Host "🔎 Checking Kubernetes cluster info..."
kubectl cluster-info

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to get cluster info. Minikube might not be running."
    exit 1
} else {
    Write-Host "Kubernetes cluster is running!"
}


# List available pods

Write-Host "Retrieving available pods..."
kubectl get pods --all-namespaces

Write-Host "All done! Kubernetes cluster is up and running."
