```python
import subprocess

def get_nodes():
    cmd = ["kubectl", "--kubeconfig=/<pathtodirectory>/modaltokai-kubeconfig.yaml", "get", "nodes"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = process.communicate()
    
    if process.returncode != 0:
        print("Error executing command:", ' '.join(cmd))
        print("Output:", out.decode())
        if err:
            print("Error:", err.decode())
        return None
    
    return out.decode()

def connect_cluster_with_kubectl_and_doctl():
    cmd_kubectl = ["kubectl", "cluster-info"]
    cmd_doctl = ["doctl", "kubernetes", "cluster", "kubeconfig", "save", "<cluster-name>"]

    process_kubectl = subprocess.Popen(cmd_kubectl, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_doctl = subprocess.Popen(cmd_doctl, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    out_kubectl, err_kubectl = process_kubectl.communicate()
    out_doctl, err_doctl = process_doctl.communicate()

    if process_kubectl.returncode != 0 or process_doctl.returncode != 0:
        print("Error executing commands")
        print("kubectl output:", out_kubectl.decode())
        print("doctl output:", out_doctl.decode())

        if err_kubectl:
            print("kubectl error:", err_kubectl.decode())
        if err_doctl:
            print("doctl error:", err_doctl.decode())

        return None

    return out_kubectl.decode(), out_doctl.decode()

def check_cert_manager():
    check_helm_cmd = ["helm", "ls", "-n", "cert-manager"]
    check_pods_cmd = ["kubectl", "get", "pods", "-n", "cert-manager"]

    helm_process = subprocess.Popen(check_helm_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pods_process = subprocess.Popen(check_pods_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    out_check_helm, err_check_helm = helm_process.communicate()
    out_check_pods, err_check_pods = pods_process.communicate()

    if helm_process.returncode != 0 || pods_process.returncode != 0:
        print("Error executing commands")
        print("Helm check output:", out_check_helm.decode())
        print("Pods check output:", out_check_pods.decode())

        if err_check_helm:
            print("Helm check error:", err_check_helm.decode())
        if err_check_pods:
            print("Pods check error:", err_check_pods.decode())

        return None

    return out_check_helm.decode(), out_check_pods.decode()
```