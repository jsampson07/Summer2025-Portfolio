from hashmap import HashMap
from json import JSONDecodeError
import requests
import re
import sys

URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
KEY = "?key=655c3343-ce3e-4449-837d-90f16da28754"

def load_wordlist(path):
    dict = HashMap(1000)
    with open(path, 'r') as f:
        for line in f.readlines():
            clean_line = line.strip()
            lowercase = clean_line.lower()
            dict.put(lowercase, True)
    return dict

def get_definition(word):
    final_url = URL + word + KEY
    response = requests.get(final_url)
    response.raise_for_status()
    json_data = response.json()
    if not json_data or isinstance(json_data[0], str): #no data returned or empty str/unexpected response value
        return None
    try:
        sseq_value = json_data[0]['def'][0]['sseq']
        dt_dict = sseq_value[0][0][1]
        defintion = dt_dict['dt'][0][1]
    except (KeyError, IndexError, TypeError):
        return None
    clean = re.sub(r"\{/?it\}", "", defintion)
    return clean

def prompt_yn():
    answer = input("Would you like to keep looking up words? [Y/n]: ").strip().lower()
    if answer in ["y", "yes"]:
        return True
    else:
        return False

def main():
    #Now I have a filled in hashmap
    #I want to take in a word from the user and see if it is in dict, if yes ==> True, else ==> False
    wordlist = "/usr/share/dict/american-english-large"
    dict_map = load_wordlist(wordlist)
    while True:
        word = input("What word would you like to lookup?: ").strip().lower()
        print()
        if word is None:
            break
        if dict_map.containsKey(word):
            print(f"{word} is in the wordlist. Fetching definition...\n")
            try:
                definition = get_definition(word)
            except JSONDecodeError as e:
                print(f"Error fetching the defintion: {e}\n")
            else:
                if definition:
                    print(f"{word}: {definition}")
                else:
                    print(f"Defintion for {word} could not be found")
        else:
            print(f"{word} is not in the wordlist")
        print()
        if not prompt_yn():
            print("Please make sure you put 'Y', 'y', or 'yes' if you wished to continue.")
            break
        print()
    print(f"Application exiting...")
    sys.exit(0)

if __name__ == "__main__":
    main()