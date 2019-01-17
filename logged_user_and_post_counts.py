
import math
import os
import pickle
import sys
from collections import defaultdict

readDir = sys.argv[1]

post_counts = defaultdict(lambda: 0)
user_counts = defaultdict(lambda: set())

for f in os.listdir(readDir):
	if f[:2] == "RS":
		with open(f, "r") as reader:
			for line in reader:
				line = line.split("\t")
				sub = line[2]
				post_counts[sub] += 1
	elif f[:2] == "RC":
		with open(f, "r") as reader:
			users = set()
			for line in reader:
				line = line.split("\t")
				sub = line[2]
				user = line[3]
				user_counts[sub].add(user)

pickle.dump(post_counts, open("post_counts.p", "wb"))
pickle.dump(user_counts, open("user_counts.p", "wb"))

post_counts = [(key, math.log(1 + post_counts[key])) for key, value in user_counts.keys()]
post_counts.sort(key=lambda x: x[1])
with open("logged_post_counts.txt", "a") as writer:
	for tup in post_counts:
		writer.write("{},\t{}\n".format(tup[0], tup[1]))
				
user_counts = [(key, math.log(1 + len(user_counts[key])) for key in user_counts.keys()]
user_counts.sort(key=lambda x: x[1]
with open("logged_user_counts.txt", "a") as writer:
	for tup in user_counts:
		writer.write("{},\t{}\n".format(tup[0], tup[1]))
