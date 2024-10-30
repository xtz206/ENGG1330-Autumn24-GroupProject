def log_to_file(msg):
    with open("./logs.txt", 'a') as f:
        f.write(msg + '\n')
