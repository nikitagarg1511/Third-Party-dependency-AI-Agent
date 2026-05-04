import requests

def get_score_from_osv_id(osv_id):
    """Deep lookup for a specific OSV/CVE ID to find a numeric score."""
    try:
        url = f"https://api.osv.dev/v1/vulns/{osv_id}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            # Search severity block in the aliased record
            for s in data.get('severity', []):
                score = s.get('score')
                try: return float(score)
                except: continue
    except: pass
    return None

def test_osv_vulnerability_check(purl):
    print(f"\n🔍 Analyzing: {purl}")
    url = "https://api.osv.dev/v1/query"
    
    try:
        response = requests.post(url, json={"package": {"purl": purl}}, timeout=10)
        data = response.json()
        vulns = data.get('vulns', [])

        if not vulns:
            print("✅ Clean.")
            return

        all_scores = []
        for v in vulns:
            v_id = v.get('id')
            score = 0.0
            
            # 1. Check current record for a numeric score
            for s in v.get('severity', []):
                try: score = max(score, float(s.get('score')))
                except: pass
            
            # 2. IF STILL 0.0: Check Aliases (This is the fix for PYSEC/GHSA)
            if score == 0.0:
                for alias in v.get('aliases', []):
                    # We prioritize CVEs as they have the most reliable numeric scores
                    if alias.startswith("CVE-") or alias.startswith("GHSA-"):
                        alias_score = get_score_from_osv_id(alias)
                        if alias_score:
                            score = max(score, alias_score)
                            break # Found a score, move to next vulnerability

            all_scores.append(score)
            print(f"   - {v_id}: Score -> {score}")

        max_score = max(all_scores) if all_scores else 0.0
        print(f"\n🏆 RESULT: Max CVSS {max_score} | {'❌ REJECT' if max_score >= 9.0 else '✅ ALLOW'}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    # PyYAML 5.3 contains CVE-2020-1747 (Critical 9.8)
    test_osv_vulnerability_check("pkg:pypi/PyYAML@5.3")
    # Requests 2.6.0 contains CVE-2015-2296 (Medium/High)
    test_osv_vulnerability_check("pkg:pypi/requests@2.6.0")