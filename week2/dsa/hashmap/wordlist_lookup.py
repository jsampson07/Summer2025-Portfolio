from hashmap import HashMap

def main():
    dict_file = '/usr/share/dict/words'
    lines = []
    with open(dict_file, 'r') as f:
        for line in f.readlines:
            lines.append(line)
    print(lines)

if __name__ == "__main__":
    main()