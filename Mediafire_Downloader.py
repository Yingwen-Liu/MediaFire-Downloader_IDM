import json
import requests
from bs4 import BeautifulSoup
import os


def get_link(url):
    """Parse the Mediafire url to get the download link"""
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        tag = soup.find(class_='input popsok')
        return tag['href']

    else:
        raise Exception(f"Error {res.status_code}: Failed to find url")


def IDM_download(url, IDM_path):
    """Download the file using Internet Download Manager"""
    import subprocess
    
    command = [IDM_path, '/d', url]
    subprocess.run(command)


def download(url, save_path):
    """Save the file in the link to the given path"""
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(res.content)
    else:
        raise Exception(f"Error {res.status_code}: Download link invalid")


def main():
    # Read the configuration
    with open('./config.json', 'r') as f:
        config = json.load(f)
    
    urls_path = config["urls_path"]
    save_dir = config["save_dir"]
    IDM_path = config["IDM_path"]
    
    # Check if Internet Download Manager is installed
    IDM = True
    if not os.path.isfile(IDM_path):
        IDM = False
        print("Warning: Internet Download Manager not found")
    
    # Convert the Mediafire urls to a list
    with open(urls_path, 'r') as f:
        urls = f.read()
    urls = urls.split("\n")
    while '' in urls:
        urls.remove('')

    # Download files from the urls
    for url in urls:
        url = url.strip()
        
        # Check if the url and the download link are valid
        try:
            download_link = get_link(url)
        except TypeError:
            print(f"Error: Failed to find the download link of {url}")
            continue
        except Exception as e:
            print(e)
            continue

        filename = download_link.split('/')[-1]
        save_path = os.path.join(save_dir, filename)
        print("Downloading " + filename)

        try:                
            if IDM:
                IDM_download(download_link, IDM_path)
            else:
                download(download_link, save_path)
            print("> Download Successfully")
                
        except Exception as e:
            print(e)
        
    print("\nAll Files Downloaded")


if __name__ == "__main__":
    main()
