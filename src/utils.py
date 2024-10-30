def log_to_file(msg):
    with open("./logs.txt", 'a') as f:
        f.write(msg + '\n')

def json_format(path):
    import json

    with open(path, 'r') as f:
        data = json.load(f)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    json_format("assets/mazes.json")
