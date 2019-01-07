import re
import sys

firstYear = int(sys.argv[1])
lastYear = int(sys.argv[2])
firstMonth = int(sys.argv[3])
lastMonth = int(sys.argv[4])

for year in range(firstYear, lastYear + 1):
  for month in range(firstMonth, lastMonth + 1):
    with open("RS_{}-{}.tsv".format(year, month), "r") as reader:
      for line in reader:
        line = line.split("\t")
        subreddit = line[2]
        submission = re.sub("[^a-z0-9]", " ", line[7].lower())
        submission = re.sub("\s+", " ", submission)
        fname = "{}-{}-{}-{}-{}.txt".format(subreddit, firstYear, lastYear, firstMonth, lastMonth)
        with open(fname, "a+") as writer:
          writer.write(" {} ".format(submission)
