# S3 Automation with Boto3

This project provides simple Python scripts to automate common AWS S3 bucket tasks using the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library. You can upload files, list files in a bucket, and delete files, all from your local machine.

## Tools Used

- **Python 3**: The programming language for all scripts.
- **boto3**: AWS SDK for Python, used to interact with S3.
- **botocore**: Low-level AWS service access, required by boto3.
- **Virtual Environment**: Keeps dependencies isolated for this project.

## Setup & Usage

1. **Clone the repository** and open the folder in VS Code or your terminal.

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    # On Windows (Command Prompt)
    venv\Scripts\activate
    # On Windows (Git Bash or PowerShell)
    source venv/Scripts/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure your AWS credentials**  
   Make sure you have your AWS credentials set up (using `aws configure` or environment variables).

5. **Edit `variables.py`**  
   Set your AWS region, bucket name, local file path, and object name as needed.

6. **Run the main script**:

    ```bash
    python main.py
    ```

## What the Scripts Do

- **Upload a file** to S3 if it does not already exist.
- **List all files** in your S3 bucket.
- **Delete a file** (optional, by uncommenting a line in `main.py`).

---

**Tip:**  
If you are new to AWS or Python, take it step by step and check the comments in
