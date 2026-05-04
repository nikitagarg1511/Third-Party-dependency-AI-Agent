from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config import api_key, SONATYPE_USER, SONATYPE_TOKEN
from tools import check_license, list_csv_columns, get_csv_rows, check_vulnerabilities, save_results_to_csv
import os

# ✅ LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# ✅ Prompt

SYSTEM_PROMPT = """
You are an Autonomous Supply Chain Security Analyst.

ALLOWED LICENSES: MIT, Apache-2.0, BSD-3-Clause,PSF-2.0, ISC.
SECURITY POLICY: Any component with a CVSS score >= 9.0 must be marked as "REJECTED - Security".


PROCESS FLOW FOR EACH ROW:
1. **Identify**: Get repo_name, artifact_name, and version from the CSV.
2. **Check_license**: Call 'check_license'. 
   - If the license is NOT in [MIT, Apache-2.0, BSD-3-Clause, PSF-2.0, ISC]:
     - Set Status="REJECTED - License", CVSS=0.0, Recommendation="Blocked due to License". 
     - SKIP check_vulnerability for this row.
3. **Vulnerability Check**: If license is allowed:
   - Construct PURL:
     * PyPI: pkg:pypi/name@version
     * NPM: pkg:npm/name@version
     * Go: pkg:golang/name@version
   - Call 'check_vulnerabilities' with ONLY the purl.
   - If Max CVSS >= 9.0: Status="REJECTED - Security", Recommendation="Blocked due to Critical Vulnerability".
   - Else: Status="APPROVED", Recommendation="None".

STRICT RULES:
- If the check_vulnerabilities tool returns any ERROR (401, 500, or Critical Error), do not retry. Instead, set the cvss_score to 0.0, set the status to 'ERROR - Check Logs', and move to the next package immediately.
- Only call tools once per package.
- Do not guess results. If a tool fails, report the error in the 'license' or 'cvss_score' column.
- After processing ALL rows, call 'save_results_to_csv' with the final JSON array.
- DO NOT summarize in text until AFTER the file is saved.
Ensure the JSON objects contain ALL fields: [repo_name, artifact_name, version, license, cvss_score, status, recommendation].

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# ✅ Agent
agent = create_openai_tools_agent(
    llm=llm,
    tools=[list_csv_columns, get_csv_rows,check_license,check_vulnerabilities,save_results_to_csv],
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[list_csv_columns, get_csv_rows,check_license,check_vulnerabilities,save_results_to_csv],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=15,               # Prevents infinite loops
    early_stopping_method="force"
)

# ✅ Run
if __name__ == "__main__":
    file_name = "input.csv"
    
    print(f"🚀 Starting autonomous analysis of {file_name}...")
    print(f"DEBUG: User is {SONATYPE_USER} and Token exists: {bool(SONATYPE_TOKEN)}")
    
    # The agent now handles the analysis AND the saving
    response = agent_executor.invoke({
        "input": f"Analyze the package list in '{file_name}' and save the results."
    })

    print("\n--- AGENT SUMMARY ---")
    print(response["output"])

   