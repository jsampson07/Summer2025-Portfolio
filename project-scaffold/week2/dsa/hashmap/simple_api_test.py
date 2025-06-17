import requests

def main():
    url = "https://dictionaryapi.com/api/v3/references/thesaurus/json/dingaling?key=655c3343-ce3e-4449-837d-90f16da28754"
    response = requests.get(url)
    resp_json = response.json()
    print(resp_json)

if __name__ == "__main__":
    main()