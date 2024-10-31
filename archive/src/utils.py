def log_to_file(*msgs, sep=" ", end="\n"):
    with open("./logs.txt", 'a') as f:
        f.write(sep.join([format(msg) for msg in msgs]) + end)

def json_format(path):
    import json

    
    with open(path, 'r') as f:
        data = json.load(f)
    if data is None:
        return
    else:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

def check_maze(maze):
    height = maze["height"]
    width = maze["width"]
    start = maze["start"]
    end = maze["end"]
    routes = maze["routes"]
    blocks = maze["block_names"]


    if len(blocks) != height * width:
        return False

    if blocks[start[0] * width + start[1]] != "start":
        return False
    
    if blocks[end[0] * width + end[1]] != "end":
        return False
    
    for route in routes:
        for block in route:
            if blocks[block[0] * width + block[1]] != "air":
                return False
    
    return True


def check_mazes(path):
    with open(path, 'r') as f:
        data = json.load(f)
    for index, maze in enumerate(data):
        if not check_maze(maze):
            print(f"Maze {index} has problems")


if __name__ == "__main__":
    # json_format("assets/mazes.json")
    check_mazes("assets/mazes.json")
