import threading
from dynamodb import write_item


def execute(item):
    print("Thread begin execute", threading.current_thread().name)
    write_item(item)
    print("Thread end execute", threading.current_thread().name)


def process():
    t1 = threading.Thread(target=execute, args=(1,))
    t2 = threading.Thread(target=execute, args=(2,))
    t3 = threading.Thread(target=execute, args=(3,))

    print("--BEGIN-THREADS--")

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("--END-THREADS--")


if __name__ == "__main__":
    process()
