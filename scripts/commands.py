import subprocess, requests
def execute_shell(cmd):
    try:
        r = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return r.decode('utf-8', errors='ignore')
    except Exception as e: return f"Shell error: {e}"
def google_search(q): return f"Simulated search: {q}"
def browse_website(url, q=None):
    try: return requests.get(url, timeout=5).text[:500]
    except Exception as e: return f"Browse error: {e}"
