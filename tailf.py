import time


def follow(fi):
    fi.seek(0, 2)
    while True:
        line = fi.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


log_file = open('test.txt')
for ln in follow(log_file):
    print(ln)
