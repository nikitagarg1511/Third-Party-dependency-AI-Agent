from pydantic import BaseModel, Field

class LicenseInput(BaseModel):
    repo_name: str = Field(description="Ecosystem like pypi, npm, go")
    artifact_name: str = Field(description="Package name")
    version: str = Field(description="Version")

class VulnerabilityInput(BaseModel):
    purl: str = Field(description="The Package URL (purl) for the component (e.g., 'pkg:pypi/requests@2.28.1')")