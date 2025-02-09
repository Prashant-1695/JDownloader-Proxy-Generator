import requests
from bs4 import BeautifulSoup

def fetch_proxies():
    url = "https://www.sslproxies.org/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        proxies = []
        table = soup.find("table", {"class": "table table-striped table-bordered"})
        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all("td")
                if len(cols) >= 5:  # Ensure all required columns are present
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxy_type = "HTTPS"  # Default type for this source
                    proxies.append((ip, port, proxy_type))

        return proxies

    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def save_proxies_to_file(proxies, filename="jdownloader_proxies.txt"):
    try:
        with open(filename, "w") as file:
            for proxy in proxies:
                ip, port, proxy_type = proxy
                file.write(f"{proxy_type} {ip}:{port}\n")  # Format: TYPE IP:PORT
        print(f"Proxies saved to {filename}")
    except Exception as e:
        print(f"Error saving proxies to file: {e}")

if __name__ == "__main__":
    proxies = fetch_proxies()
    if proxies:
        save_proxies_to_file(proxies)
    else:
        print("No proxies fetched.")
