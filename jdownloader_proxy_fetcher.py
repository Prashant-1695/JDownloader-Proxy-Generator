import requests
from bs4 import BeautifulSoup

def fetch_https_proxies():
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
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.append(("HTTPS", ip, port))

        return proxies

    except Exception as e:
        print(f"Error fetching HTTPS proxies: {e}")
        return []

def fetch_socks_proxies():
    url = "https://www.socks-proxy.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        proxies = []
        table = soup.find("table", {"id": "proxylisttable"})
        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all("td")
                if len(cols) >= 5:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxy_type = cols[4].text.strip().upper()  # SOCKS4 or SOCKS5
                    proxies.append((proxy_type, ip, port))

        return proxies

    except Exception as e:
        print(f"Error fetching SOCKS proxies: {e}")
        return []

def save_proxies_to_file(proxies, filename="jdownloader_proxies.txt"):
    try:
        with open(filename, "w") as file:
            for proxy in proxies:
                proxy_type, ip, port = proxy
                file.write(f"{proxy_type} {ip}:{port}\n")  # Format: TYPE IP:PORT
        print(f"Proxies saved to {filename}")
    except Exception as e:
        print(f"Error saving proxies to file: {e}")

if __name__ == "__main__":
    # Fetch proxies from both sources
    https_proxies = fetch_https_proxies()
    socks_proxies = fetch_socks_proxies()

    # Combine the proxy lists
    all_proxies = https_proxies + socks_proxies

    if all_proxies:
        save_proxies_to_file(all_proxies)
    else:
        print("No proxies fetched.")