import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog='Advent of Code 2024')
    parser.add_argument('puzzle_input', type=argparse.FileType('r'))
    parser.add_argument('--submit', type=int)
    args = parser.parse_args()
    return args
