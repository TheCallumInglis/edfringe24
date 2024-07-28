# EdFringe 2024 Show Planner

## Introduction

This repository helps coordinate the shows that friends plan to see at the Edinburgh Fringe Festival. Each user can upload a CSV file of the shows they plan to attend, and the system will generate a combined plan indicating which shows everyone is attending together.

It has been designed to work with exports from [Plan My Fringe](https://planmyfringe.co.uk/), on the __My Schedule__ page, click __Export__ and select __CSV__.

## Repository Structure
```
.
├── .github
│ ├── workflows
│ │ └── check_uploads.yml
│ ├── scripts
│ │ └── check_uploads.py
├── uploads
│ ├── user1
│ │ └── upload.csv
│ ├── user2
│ │ └── upload.csv
├── planner
├── scripts
│ └── gen_plan.py
├── README.md
```

- **.github/workflows/check_uploads.yml**: GitHub Actions workflow to check uploads and generate the plan.
- **.github/scripts/check_uploads.py**: Script to ensure each user's upload directory contains exactly one CSV file.
- **uploads/**: Directory where each user uploads their CSV file.
- **planner/**: Directory where the generated plan is stored. Previous plans are moved to a timestamped directory under `planner/archive/`.
- **scripts/gen_plan.py**: Script to generate the combined plan from users' CSV files.
- **README.md**: This file.

## Usage

### Uploading CSV Files

1. Each user should upload their CSV file to their respective directory in the `uploads` folder.
2. The CSV file should have the following columns:
   - Date
   - Name
   - Rating
   - Walk to Show
   - Price(£)
   - Start Time
   - End Time
   - Duration
   - Venue

### Generating the Plan

1. The GitHub Actions workflow runs automatically on any pull request that affects files in the `uploads/**` path.
2. The workflow will:
   - Check that each user directory in `uploads/` contains exactly one CSV file.
   - Run the `generate_plan.py` script to generate a combined plan.
   - Move previous plans to a timestamped directory under `planner/active/`.
   - Commit the new plan to the `planner` directory and create a pull request.

## Running Locally

To run the plan generation script locally:

1. Ensure you have Python and the required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python scripts/gen_plan.py
   ``` 

## Contributing
Fork the repository.
Create a new branch for your feature or bugfix.
Make your changes and commit them.
Push your changes to your fork.
Create a pull request to merge your changes into the main repository.
Creating a Pull Request
Make sure your branch is up-to-date with the main branch.
Open a pull request from your branch to the main branch.
Describe your changes and why they are necessary.
The GitHub Actions workflow will run to ensure your changes are valid.