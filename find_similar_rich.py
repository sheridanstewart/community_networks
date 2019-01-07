import pickle
import numpy as np
import sys
from prettytable import PrettyTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.metrics.pairwise import linear_kernel

try:
	assert len(sys.argv) >= 4
except:
	print("Usage: python find_similar.py directory pickleflag subreddits num_matches")
	
dir_ = sys.argv[1]
pickleFlag = sys.argv[2]
subreddits = sys.argv[3:-3]
n = int(sys.argv[-3])
method = sys.argv[-2]
log = sys.argv[-1]

try:
	assert method in ["average", "max"]
	assert log in ["t", "true", "f", "false"]
except:
	print("Usage: python find_similar_rich.py directory pickleflag subreddits num_matches method logtruefalse")
	print("Methods: average, max")
	print("Log: true or false")

subredditlist = pickle.load(open("{}_subredditlist.p".format(pickleFlag), "rb"))

if n >= len(subredditlist):
	n = len(subredditlist) - 1
	
user_counts = pickle.load(open("{}_user_counts.p".format(pickleFlag), "rb"))
assert len(subredditlist) == len(user_counts)

if not log:
	user_matrix = pickle.load(open("{}_tfidf_matrix_raw_users.p".format(pickleFlag), "rb"))
	content_matrix = pickle.load(open("{}_tfidf_matrix_raw_content.p".format(pickleFlag), "rb"))
	assert len(subredditlist) == tfidf_matrix_raw.shape[0]
else:
	user_matrix = pickle.load(open("{}_tfidf_matrix_logged_users.p".format(pickleFlag), "rb"))
	content_matrix = pickle.load(open("{}_tfidf_matrix_logged_content.p".format(pickleFlag), "rb"))
	assert len(subredditlist) == tf_idf_matrix_logged.shape[0]


def find_similar(matrix1, matrix2, index, top_n):
	#sims = linear_kernel(matrix[index:index+1], matrix).flatten() # relies on l2 norm; import commented out
	sims1 = cosine_similarity(matrix1[index:index+1], matrix1).flatten() # no normalization needed
	sims2 = cosine_similarity(matrix2[index:index+1], matrix2).flatten()
	if method == "max":
		sims = np.maximum(sims1, sims2)
	else:
		sims = (sims1 + sims2)/2
	related_docs_indices = [i for i in sims.argsort()[::-1] if i != index]
	return [(index, sims[index]) for index in related_docs_indices][0:top_n]


for subreddit in subreddits:
	cols = ["Top {} Matches for {}:".format(n, subreddit), "Cosine:", "Users:"]
	matches = []
	scores = []
	counts = []
	table = PrettyTable()
	subreddit_index = subredditlist.index(subreddit)
	for index, score in find_similar_rich(user_matrix, content_matrix, subreddit_index, n):
		matches.append(subreddlist[index])
		scores.append(score)
		counts.append(user_counts[index])
	table.add_column(cols[0], matches)
	table.add_column(cols[1], scores)
	table.add_column(cols[2], counts)
	print(table)
	print("")
