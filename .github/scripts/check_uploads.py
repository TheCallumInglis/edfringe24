import os
import sys

# Path to the uploads folder
UPLOADS_FOLDER = 'uploads'

def check_uploads_folder():
    for root, dirs, files in os.walk(UPLOADS_FOLDER):
        if root == UPLOADS_FOLDER:
            for dir_name in dirs:
                user_folder = os.path.join(root, dir_name)
                csv_files = [f for f in os.listdir(user_folder) if f.endswith('.csv')]
                if len(csv_files) != 1:
                    print(f"Error: {user_folder} contains {len(csv_files)} CSV files. Each user folder must contain exactly one CSV file.")
                    sys.exit(1)
    print("All user folders contain exactly one CSV file.")

if __name__ == "__main__":
    check_uploads_folder()
