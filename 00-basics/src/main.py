import time as T
import os

def main(name:str):
    print("Hello {}".format(name),flush=True)
    T.sleep(int(os.environ.get("WAIT","5")))


if __name__ == "__main__":
    main(os.environ.get("NAME","Guest"))
