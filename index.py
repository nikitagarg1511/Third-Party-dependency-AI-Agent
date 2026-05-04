from pydantic import BaseModel, Field
import requests

class LicenseInput(BaseModel):
    repo_name: str
    artifact_name: str
    version: str

def check_license(repo_name: str, artifact_name: str, version: str) -> str:
    try:
        url = f"https://pypi.org/pypi/{artifact_name}/{version}/json"
        print(f"[DEBUG] Calling PyPI API: {url}")

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return f"Failed to fetch data for {artifact_name}=={version}"

        data = response.json()

        license_name = data["info"].get("license")
        classifiers = data["info"].get("classifiers", [])

        license_classifier = [
            c for c in classifiers if "License" in c
        ]

        if license_name:
            return f"{artifact_name}=={version} License: {license_name}"

        elif license_classifier:
            return f"{artifact_name}=={version} License: {license_classifier[0]}"

        else:
            return f"{artifact_name}=={version} License: Not found"

    except Exception as e:
        return f"Error: {str(e)}"


# ✅ Run test
if __name__ == "__main__":
    result = check_license(
        repo_name="demo",
        artifact_name="requests",
        version="2.31.0"
    )
    print("\nResult:", result)