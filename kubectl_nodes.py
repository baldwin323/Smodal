```python
import logging
from kubernetes import client, config

def connect_cluster_with_kubectl_and_doctl():
    try:
        config.load_kube_config('<cluster-name>')
        print("Connected to cluster:")
        
    except Exception as e:
        logging.error(f"Unable to connect to the cluster: {str(e)}")

def get_nodes():
    try:
        v1 = client.CoreV1Api()
        logging.info("Listing nodes with their IPs:")
        ret = v1.list_node(pretty=True)

        for i in ret.items:
            logging.info(f'{i.metadata.name} \t{i.status.addresses[0].address}')
            
    except Exception as e:
        logging.error(f"Failed to fetch nodes: {str(e)}")

def check_cert_manager():
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        logging.info("Listing pods in 'cert-manager' namespace:")
        ret = v1.list_namespaced_pod(namespace='cert-manager')
       
        helm_check = client.RbacAuthorizationV1Api().list_role_binding(namespace='cert-manager', field_selector='metadata.name=helm')

        if helm_check.items:
            logging.info("Helm is installed in the 'cert-manager' namespace.")
        else:
            logging.info("Helm is not installed in the 'cert-manager' namespace.")
        
        for i in ret.items:
            logging.info(f'{i.status.pod_ip} \t{i.metadata.namespace} \t{i.metadata.name}')
            
    except Exception as e:
        logging.error(f"Failed to check cert manager: {str(e)}")
```