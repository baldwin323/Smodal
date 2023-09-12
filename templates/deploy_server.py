```python
import sys

def setup_python_server():
    print("To set up the Python server to listen on 0.0.0.0:3000, follow these steps:")
    print("1. Open the manage.py file in your Django project.")
    print("2. Locate the main() function.")
    print("3. Look for the line execute_from_command_line(sys.argv).")
    print("4. Replace that line with the following code:")
    print("   from django.core.management.commands.runserver import Command as runserver")
    print("   runserver.default_addr = '0.0.0.0'")
    print("   runserver.default_port = '3000'")
    print("   runserver.default_ipv6 = False")
    print("   runserver.default_use_ipv6 = False")
    print("   execute_from_command_line([sys.argv[0], 'runserver'])")
    print("5. Save the manage.py file.")
    print("This will configure the server to listen on 0.0.0.0:3000, allowing access from external sources.")

def print_filename():
    filenames = ['/Smodal/templates/nav.html']  # Replace with actual filenames in the directory
    existing_filenames = set(filenames)
    new_filename = "util.py" 

    while new_filename in existing_filenames:
        new_filename = input("Enter a filename (should not already exist in the directory): ") 

    print(new_filename)

if __name__ == "__main__":
    setup_python_server()
    print()
    print_filename()
```