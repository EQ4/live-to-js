#!/usr/bin/python

import sys

def main():
    file = open("test.pd", 'w')
    file.write("hello world")
    file.close()

if __name__ == "__main__":
    main()
