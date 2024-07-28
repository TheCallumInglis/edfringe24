import pandas as pd
import os
from datetime import datetime
import shutil

# Define paths
UPLOADS_FOLDER = 'uploads'
PLANNER_FOLDER = 'planner'
PLANNER_FOLDER_ARCHIVE = os.path.join(PLANNER_FOLDER, 'archive')

IMPORT_COLUMNS = ['Date', 'Name', 'Rating', 'Walk to Show', 'Price(£)', 'Start Time', 'End Time', 'Duration', 'Venue']
REQUIRED_COLUMNS = ['Name', 'Start Time', 'End Time', 'Duration', 'Venue']

def collect_csv_files():
    csv_files = {}
    for root, dirs, files in os.walk(UPLOADS_FOLDER):
        for file in files:
            if file.endswith('.csv'):
                username = os.path.basename(root)
                if username not in csv_files:
                    csv_files[username] = []
                csv_files[username].append(os.path.join(root, file))
    return csv_files

def process_csv_files(csv_files):
    all_shows = []
    
    for username, files in csv_files.items():
        if len(files) > 1:
            print(f"Error: More than one CSV file found for user {username}. Please ensure there is only one CSV file per user.")
            return pd.DataFrame()

        user_data = []
        voter_column = f'Voter: {username}'

        for file in files:
            df = pd.read_csv(file, skipinitialspace=True, usecols=IMPORT_COLUMNS)
            print(f"Processing file: {file} for user: {username}")
            print("DataFrame head before filtering:")
            print(df.head())

            # Keep only the required columns, if they exist
            if all(col in df.columns for col in REQUIRED_COLUMNS):
                df = df[REQUIRED_COLUMNS]
                df[voter_column] = 'X'  # Add the username column with 'X'
                user_data.append(df)
            else:
                print(f"File {file} is missing required columns.")
        
        if user_data:
            user_df = pd.concat(user_data)
            all_shows.append(user_df)
    
    if not all_shows:
        print("No valid shows found in CSV files.")
        return pd.DataFrame()
    
    # Combine all shows into a single DataFrame
    combined_df = pd.concat(all_shows, ignore_index=True)
    
    # Pivot to ensure each show appears once with all users marked
    combined_df = combined_df.pivot_table(index=REQUIRED_COLUMNS, aggfunc='first', fill_value='')
    combined_df = combined_df.reset_index()
    
    return combined_df

def archive_old_plans():
    # Create the archive folder if it doesn't exist
    os.makedirs(PLANNER_FOLDER_ARCHIVE, exist_ok=True)

    # Create a timestamped subfolder in the archive folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_folder = os.path.join(PLANNER_FOLDER_ARCHIVE, timestamp)
    os.makedirs(archive_folder, exist_ok=True)

    # Move all files from the planner folder to the timestamped subfolder
    for file_name in os.listdir(PLANNER_FOLDER):
        file_path = os.path.join(PLANNER_FOLDER, file_name)
        if os.path.isfile(file_path):
            shutil.move(file_path, archive_folder)

def save_combined_df(combined_df):
    if combined_df.empty:
        print("No data to save.")
        return
    
    # Ensure the columns are in the correct order
    user_columns = [col for col in combined_df.columns if col not in REQUIRED_COLUMNS]
    column_order = REQUIRED_COLUMNS + user_columns

    combined_df['Total Votes'] = combined_df[user_columns].apply(lambda row: row.eq('X').sum(), axis=1)

    combined_df = combined_df[column_order + ['Total Votes']]

    # Archive Old Plans
    archive_old_plans()

    # Create the planner folder if it doesn't exist
    os.makedirs(PLANNER_FOLDER, exist_ok=True)
    
    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f'{PLANNER_FOLDER}/plan_{timestamp}.csv'
    
    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_file, index=False)
    print(f'Plan generated: {output_file}')

if __name__ == "__main__":
    csv_files = collect_csv_files()
    combined_df = process_csv_files(csv_files)
    save_combined_df(combined_df)
