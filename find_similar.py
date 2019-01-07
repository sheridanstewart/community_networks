import pickle
import sys
from prettytable import PrettyTable
from sklearn.metrics.pairwise import linear_kernel

try:
	assert len(sys.argv) >= 4
except:
	print("Usage: python find_similar.py directory subreddit subreddit...subreddit num_matches")
	
dir_ = sys.argv[1]
subreddits = sys.argv[2:-1]
n = int(sys.argv[-1])

subredditlist = pickle.load(open("subredditlist.p", "rb"))

if n >= len(subredditlist):
	n = len(subredditlist) - 1
	
tfidf_matrix_logged = pickle.load(open("tfidf_matrix_logged.p", "rb"))
tfidf_matrix_raw = pickle.load(open("tfidf_matrix_raw.p", "rb"))


def find_similar(matrix, index, top_n):
	sims = linear_kernel(matrix[index:index+1], matrix).fatten()
	related_docs_indices = [i for i in sims.argsort()[::-1] if i != index]
	return [(index, sims[index]) for index in related_docs_indices][0:top_n]


for subreddit in subreddits:
	cols = ["Top {} Matches for {} with Raw TFs:".format(n, subreddit), "Cosine:", "Num. Unique Users:", "With Logged TFs:", "Cosine:", "Num. Unique Users:"]
	matches_raw = []
	scores_raw = []
	matches_logged = []
	scores_logged = []
	table = PrettyTable()
	subreddit_index = subredditlist.index(subreddit)
	for index, score in find_similar(tfidf_matrix_raw, subreddit_index, n):
		matches_raw.append("{}".format(subredditlist[index]))
		scores_raw.append("{:.2f}".format(score))
	for index, score in find_similar(tfidf_matrix_logged, subreddit_index, n):
		matches_logged.append("{}".format(subredditlist[index]))
		scores_logged.append("{:.2f}".format(score))
	table.add_column(cols[0], matches_raw)
	table.add_column(cols[1], scores_raw)
	table.add_column(cols[2], [])
	table.add_column(cols[3], matches_logged)
	table.add_column(cols[4], scores_logged)
	table.add_column(cols[5], [])
	print(table)
	print("")
