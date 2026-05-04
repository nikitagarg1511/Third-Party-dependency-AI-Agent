# Autonomous Supply Chain Security Agent

A Python-based autonomous agent that analyzes a CSV package list, checks license compliance, validates vulnerabilities using Sonatype OSS Index, and saves a structured results CSV.

## Features

- **Autonomous analysis** of package inventories using a LangChain/OpenAI agent
- **License compliance checks** for PyPI, NPM, and Go packages
- **Vulnerability validation** with Sonatype OSS Index
- **Policy enforcement** for CVSS score and allowed licenses
- **CSV tool support** for reading columns, previewing rows, and exporting results

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/third-party-dependency-agent.git
   cd Third-Party-dependency-AI-Agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your credentials:
   ```ini
   OPENAI_API_KEY=your_openai_api_key_here
   SONATYPE_USER=your_sonatype_username
   SONATYPE_TOKEN=your_sonatype_token
   ```

## Usage

### Run the main agent

The primary entrypoint is `agent.py`.

```bash
python agent.py
```

This script uses `input.csv` by default and writes results to `output_results.csv`.

### Inspect or test individual tools

- `tools.py` defines the helper tools used by the agent
- `schemas.py` defines input schemas for tool validation
- `config.py` loads API credentials from `.env`
- `index.py` contains a standalone license lookup helper
- `hello.py` contains a second agent example and prompt template

## Configuration

- `OPENAI_API_KEY` — OpenAI API key for `ChatOpenAI`
- `SONATYPE_USER` — Sonatype OSS Index username
- `SONATYPE_TOKEN` — Sonatype OSS Index API token

## Project Workflow

1. `agent.py` builds a LangChain agent using `ChatOpenAI` and custom tools.
2. The system prompt enforces policy rules for license and vulnerability decisions.
3. `tools.py` provides:
   - `list_csv_columns` to inspect CSV headers
   - `get_csv_rows` to preview CSV data
   - `check_license` to resolve package licenses
   - `check_vulnerabilities` to query Sonatype OSS Index
   - `save_results_to_csv` to write final JSON output to CSV
4. The agent processes each package row and saves the results.

## Input / Output

- `input.csv` should contain package rows with `repo_name`, `artifact_name`, and `version` fields.
- `output_results.csv` is created by the agent and contains fields such as:
  - `repo_name`
  - `artifact_name`
  - `version`
  - `license`
  - `cvss_score`
  - `status`
  - `recommendation`

## Policy Rules

- Allowed licenses: `MIT`, `Apache-2.0`, `BSD-3-Clause`, `PSF-2.0`, `ISC`
- Packages with CVSS >= 9.0 are marked as `REJECTED - Security`
- Disallowed licenses are marked as `REJECTED - License`
- Sonatype API errors result in `ERROR - Check Logs` and a CVSS score of `0.0`

## Requirements

- Python 3.10+
- `langchain`
- `langchain-openai`
- `langchain-core`
- `pydantic`
- `requests`
- `pandas`
- `python-dotenv`

## Project Structure

```text
├── agent.py            # Main agent runner and prompt policy
├── config.py           # Environment configuration and API credentials
├── hello.py            # Alternate agent example with the same security workflow
├── index.py            # Standalone license lookup utility
├── schemas.py          # Tool input schemas for LangChain tools
├── tools.py            # Tool implementations used by the agent
├── input.csv           # Sample package inventory input
├── output_results.csv  # Generated analysis output file
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Ignored project files
```

## Notes

- Keep `.env` private and never commit credentials to source control.
- The agent is designed to make one tool call per package and to avoid retries on fatal Sonatype errors.

## Support

If you need help running the project, check your `.env` configuration and ensure your OpenAI and Sonatype credentials are valid.