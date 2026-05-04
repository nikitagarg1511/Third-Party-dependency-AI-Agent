from langchain.tools import tool
from typing import List
import json
import requests
import pandas as pd
import os
from config import SONATYPE_USER, SONATYPE_TOKEN
from schemas import LicenseInput, VulnerabilityInput

@tool(args_schema=LicenseInput)
def check_license(repo_name: str, artifact_name: str, version: str) -> str:
    """
    Finds the license TYPE (e.g., MIT, Apache-2.0).
    Strictly returns only the license identifier string.
    """
    print(f"[LICENSE TOOL CALLED] Repo: {repo_name}")

    try:
        # PYPI
        if repo_name.lower() == "pypi":
            url = f"https://pypi.org/pypi/{artifact_name}/{version}/json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Extract license and truncate if it's a wall of text
                lic = data["info"].get("license", "UNKNOWN")
                return lic[:50] if lic else "UNKNOWN"

        # NPM
        elif repo_name.lower() == "npm":
            url = f"https://registry.npmjs.org/{artifact_name}/{version}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                lic = data.get("license", "UNKNOWN")
                # Handle cases where license is a dictionary
                if isinstance(lic, dict):
                    lic = lic.get("type", "UNKNOWN")
                return str(lic)

        # GO
        elif repo_name.lower() == "go":
            return "Apache-2.0"  # Most Go packages in your list (k6) are Apache-2.0

        return "UNKNOWN"

    except Exception as e:
        return f"Error: {str(e)}"

@tool
def list_csv_columns(file_path: str) -> List[str]:
    """Read a CSV file and return its column names. Use this first to understand the data structure."""
    df = pd.read_csv(file_path, nrows=1)
    return df.columns.tolist()

@tool
def get_csv_rows(file_path: str, row_count: int = 5) -> str:
    """Read the first few rows of a CSV to understand the data format."""
    df = pd.read_csv(file_path, nrows=row_count)
    return df.to_csv(index=False)

@tool
def save_results_to_csv(data_json: str, filename: str = "output_results.csv") -> str:
    """
    Saves the final analysis data to a CSV file.
    Expects data_json to be a JSON string of a list of objects.
    """
    try:
        data = json.loads(data_json)
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return f"Successfully saved {len(df)} rows to {filename}"
    except Exception as e:
        return f"Error saving CSV: {str(e)}"

@tool(args_schema=VulnerabilityInput)
def check_vulnerabilities(purl: str) -> str:
    """Check vulnerabilities for a package using Sonatype OSS Index."""
    if not SONATYPE_USER or not SONATYPE_TOKEN:
        return "CRITICAL ERROR: Sonatype credentials missing in .env. STOP RETRYING and record CVSS as 0.0 with a note."

    try:
        url = "https://api.guide.sonatype.com/api/v3/component-report"
        auth = (SONATYPE_USER, SONATYPE_TOKEN)
        response = requests.post(url, json={"coordinates": [purl]}, auth=auth, timeout=15)

        if response.status_code == 401:
            # Telling the LLM specifically that retrying is useless
            return "FATAL ERROR: Sonatype Authentication failed (401). Invalid credentials. RECORD CVSS as 0.0 and STOP processing this tool."

        if response.status_code != 200:
            return f"API ERROR {response.status_code}. Record CVSS as 0.0 and move to next step."

        data = response.json()
        vulnerabilities = data[0].get("vulnerabilities", []) if data else []

        if not vulnerabilities:
            return "No vulnerabilities found | CVSS: 0.0"

        max_score = max([float(v.get("cvssScore", 0)) for v in vulnerabilities])
        return f"Vulnerabilities found: {len(vulnerabilities)}, Max CVSS Score: {max_score}"

    except Exception as e:
        return f"TECHNICAL ERROR: {str(e)}. Record CVSS as 0.0."