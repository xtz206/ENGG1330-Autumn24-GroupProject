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
        return False, "Block Count Unconsistent", f"Get {len(blocks)} blocks while expected {height * width} blocks"
    
    for index, block in enumerate(blocks):
        if block not in ("air", "wall", "start", "end", "bonus", "box"):
            return False, "Unknown Blocks", f"Get unknown block {block} at {index}"

    index = start[0] * width + start[1]
    if blocks[index] != "start":
        return False, "Block Start Unconsistent", f"Get {blocks[index]} at {index} while expected start"
    
    index = end[0] * width + end[1]
    if blocks[index] != "end":
        return False, "Block End Unconsistent", f"Get {blocks[index]} at {index} while expected end"
    
    for route in routes.values():
        for block in route:
            index = block[0] * width + block[1]
            if blocks[index] != "air":
                return False, "Route is Blocked", f"Get {blocks[index]} at {index} while expected air"
    
    return True, None, None

def check_mazes(path):
    with open(path, 'r') as f:
        data = json.load(f)
    count = 0
    for index, maze in enumerate(data):
        status, reason, description = check_maze(maze)
        if not status:
            print(f"Error occurs at Maze {index}")
            print(f"Reason: {reason}")
            print(f"Description: {description}")
            count += 1
    if count == 0:
        print("All Mazes Pass the Checks")

def print_helps():

    print("Usage: python utils.py [OPTIONS] [PATH]")
    print("Options: ")
    print("    -m <path>  Check the Mazes ")
    print("    -f <path>  Format the jsons")
    print("    -h         Display the help")

def main(*args, **kwargs):
    if len(args) < 2:
        print("You must specify the mode")
        print_helps()
        return
    if args[1] == "-h":
        print_helps()
        return
    if len(args) < 3:
        print("You must specify the path")
        print_helps()
        return
    if args[1] == "-m":
        check_mazes(args[2])
        return
    if args[1] == "-f":
        json_format(args[2])
        return
    else:
        print("Unknown options")
        print_helps()
        return

if __name__ == "__main__":
    main(*sys.argv)
