import json
import sys

def log_to_file(*msgs, sep=" ", end="\n"):
    with open("./logs.txt", 'a') as f:
        f.write(sep.join([format(msg) for msg in msgs]) + end)

def json_format(path):
    with open(path, 'r') as f:
        data = json.load(f)
    if data is None:
        print("Error occurs when decoding json file")
        return
    else:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        print("Formatting Successful")

def check_maze(maze):
    height = maze["height"]
    width = maze["width"]
    start = maze["start"]
    end = maze["end"]
    routes = maze.get("routes", {})
    blocks = maze["block_names"]

    if len(blocks) != height * width:
        return f"Block Count is not consistent", 0

    index = start[0] * width + start[1]
    if blocks[index] != "start":
        return f"start is not consistent", index
    
    index = end[0] * width + end[1]
    if blocks[index] != "end":
        return f"end is not consistent", index
    
    for route in routes.values():
        for block in route:
            index = block[0] * width + block[1]
            if blocks[index] != "air":
                return f"route {block} is blocked", index
    
    return None, None

def check_mazes(path):
    with open(path, 'r') as f:
        data = json.load(f)
    for index, maze in enumerate(data):
        reason, index = check_maze(maze)
        if reason is not None:
            print(f"Maze {index} has error Due to {reason} At Index {index}")

def print_helps():
    print("HELPS:")
    print("usage: python utils.py [OPTIONS] [PATH]")
    print("-m <path>  Check the Mazes")
    print("-f <path>  Format the jsons")
    print("-h         Display the help")

def main(*args, **kwargs):
    if len(args) < 2:
        print("You must specify the mode")
        return
    if args[1] == "-h":
        print_helps()
        return
    if len(args) < 3:
        print("You must specify the path")
        print_helps()
    if args[1] == "-m":
        check_mazes(args[2])
    if args[1] == "-f":
        json_format(args[2])

if __name__ == "__main__":
    main()
