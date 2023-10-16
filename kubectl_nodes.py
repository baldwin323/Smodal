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
```