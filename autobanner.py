#!/usr/bin/env python3

import random
import sys

def main():
	arguments = get_args()
	participants = set(map(int, sys.stdin.read().split()))
	number = 15 if len(participants) > 128 else 3
	winners = random.sample(participants, number)

	print("Победители:")
	for user in winners:
		print("\t{}".format(user))

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main()
	else:
		print(__doc__, file=sys.stderr)
