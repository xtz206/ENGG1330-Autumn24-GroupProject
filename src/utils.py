import json

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
    routes = maze.get("routes", {})
    blocks = maze["block_names"]

    if len(blocks) != height * width:
        return f"Block Count is not consistent", 0

    index = start[0] * width + start[1]
    if blocks[index] != "start":
        return f"Start is not consistent", index
    
    index = end[0] * width + end[1]
    if blocks[index] != "end":
        return f"End is not consistent", index
    
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
            print(f"Maze {index} has problems, Reason: {reason}, Index: {index}")


if __name__ == "__main__":
    # json_format("assets/mazes.json")
    check_mazes("assets/mazes.json")
