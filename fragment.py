import os
import subprocess
import sys

def manage_dependencies():
    libs = ["requests", "beautifulsoup4"]
    for lib in libs:
        try:
            __import__(lib.replace('beautifulsoup4', 'bs4'))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

manage_dependencies()

import requests
import re
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore")

def validator(query):
    print("\n" + "@"*30)
    print("$ SCRAPER BY: xxxxxthefox/thefox")
    print("@"*30 + "\n")
    
    session = requests.Session()
    ua = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36'
    
    try:
        res = session.get(f'https://fragment.com/?query={query}', headers={'user-agent': ua})
        h_match = re.search(r'hash=([a-f0-9]+)', res.text)
        if not h_match: return "❌ Hash Error (Try VPN)"
        
        h = h_match.group(1)
        api = 'https://fragment.com/api'
        headers = {
            'authority': 'fragment.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': ua,
            'referer': f'https://fragment.com/?query={query}',
            'origin': 'https://fragment.com',
        }
        
        payload = {'type': 'usernames', 'query': query, 'method': 'searchAuctions'}
        resp = session.post(api, params={'hash': h}, headers=headers, data=payload)
        
        if resp.status_code != 200: return f"❌ Server Error: {resp.status_code}"
        
        js = resp.json()
        if "html" not in js: return "❌ No Data"

        soup = BeautifulSoup(js["html"], 'html.parser')
        rows = soup.find_all('tr', class_='tm-row-selectable')
        if not rows: return "📭 No results"

        results = []
        for r in rows:
            u = r.find('div', class_='table-cell-value').get_text(strip=True)
            s_tag = r.find('div', class_='tm-status-avail') or r.find('div', class_='table-cell-status-thin')
            s = s_tag.get_text(strip=True) if s_tag else "N/A"
            p = r.find('div', class_='icon-before').get_text(strip=True) if r.find('div', class_='icon-before') else "0"
            results.append({"u": u, "s": s, "p": p})
        return results
    except Exception as e:
        return f"❌ {str(e)}"

target = input("Enter search query: ")
data = validator(target)

if isinstance(data, list):
    print(f"{'Username':<20} | {'Status':<15} | {'Price'}")
    print("-" * 55)
    for i in data:
        print(f"{i['u']:<20} | {i['s']:<15} | {i['p']}")
    print("\n" + "@"*30)
    print("DONE BY: xxxxxthefox/thefox")
    print("@"*30)
else:
    print(data)
