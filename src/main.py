import sys
import os
import shutil

def copy_static(src, dst):
    """
    Recursively copy contents from src directory to dst directory.
    """
    # First, delete the contents of the destination directory if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)
    
    # Create the destination directory
    os.makedirs(dst)

    # Walk through the source directory
    for root, dirs, files in os.walk(src):
        # Create corresponding subdirectories in destination
        for dir_name in dirs:
            src_path = os.path.join(root, dir_name)
            dst_path = os.path.join(dst, os.path.relpath(src_path, src))
            os.makedirs(dst_path, exist_ok=True)
            print(f"Created directory: {dst_path}")

        # Copy files
        for file_name in files:
            src_path = os.path.join(root, file_name)
            dst_path = os.path.join(dst, os.path.relpath(src_path, src))
            shutil.copy2(src_path, dst_path)
            print(f"Copied file: {dst_path}")

def main():
    # Get the project root directory (assuming main.py is in src/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Set the paths for source and destination directories
    static_dir = os.path.join(project_root, 'static')
    public_dir = os.path.join(project_root, 'public')

    # Check if static directory exists
    if not os.path.exists(static_dir):
        print(f"Error: Static directory not found at {static_dir}")
        sys.exit(1)

    # Copy static files to public directory
    copy_static(static_dir, public_dir)
    print("Static files copied successfully!")

if __name__ == "__main__":
    main()