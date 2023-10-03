```python
import os

def grant_admin_access():
    os.system("cd C:\\Python311\\Scripts")
    os.system("Takeown /f *")
    os.system("Icacls * /grant administrators:F")

grant_admin_access()
```