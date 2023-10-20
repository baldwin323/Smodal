```python
from kubernetes import client, config

def get_nodes():
    config.load_kube_config('/<pathtodirectory>/modaltokai-kubeconfig.yaml')
    v1 = client.CoreV1Api()
    print("Listing nodes with their IPs:")
    ret = v1.list_node(pretty=True)
    for i in ret.items:
        print(f'{i.metadata.name} \t{i.status.addresses[0].address}')
     

def connect_cluster_with_kubectl_and_doctl():
    config.load_kube_config('<cluster-name>')
    v1 = client.CoreV1Api()
    print("Connected to cluster:")

    print("Listing first 5 pods running in all namespaces:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items[:5]:
        msg = f'{i.status.pod_ip} \t{i.metadata.namespace} \t{i.metadata.name}'
        print(msg)


def check_cert_manager():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods in 'cert-manager' namespace:")
    ret = v1.list_namespaced_pod(namespace='cert-manager')
   
    print("Helm check:")
    helm_check = client.RbacAuthorizationV1Api().list_role_binding(namespace='cert-manager', field_selector='metadata.name=helm')

    if helm_check.items:
        print("Helm is installed in the 'cert-manager' namespace.")
    else:
        print("Helm is not installed in the 'cert-manager' namespace.")
    
    for i in ret.items:
        print(f'{i.status.pod_ip} \t{i.metadata.namespace} \t{i.metadata.name}')
```