import pickle
import sys
from prettytable import PrettyTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.metrics.pairwise import linear_kernel

try:
	assert len(sys.argv) >= 6
	assert sys.argv[-1] in ["content", "users", "user"]
except:
	print("Usage: python find_similar.py directory pickleflag subreddits num_matches contentorusers")
	print("content or users")
	
dir_ = sys.argv[1]
pickleFlag = sys.argv[2]
subreddits = sys.argv[3:-2]
n = int(sys.argv[-2])
content_or_users = sys.argv[-1]
if content_or_users == "user":
	content_or_users = "users"

subredditlist = pickle.load(open("{}_subredditlist.p".format(pickleFlag), "rb"))

if n >= len(subredditlist):
	n = len(subredditlist) - 1
	
user_counts = pickle.load(open("{}_user_counts.p".format(pickleFlag), "rb"))
assert len(subredditlist) == len(user_counts)

tfidf_matrix_raw = pickle.load(open("{}_tfidf_matrix_raw_{}.p".format(pickleFlag, content_or_users), "rb"))
assert len(subredditlist) == tfidf_matrix_raw.shape[0]

tfidf_matrix_logged = pickle.load(open("{}_tfidf_matrix_logged_{}.p".format(pickleFlag, content_or_users), "rb"))
assert len(subredditlist) == tf_idf_matrix_logged.shape[0]


def find_similar(matrix, index, top_n):
	#sims = linear_kernel(matrix[index:index+1], matrix).flatten() # relies on l2 norm; import commented out
	sims = cosine_similarity(matrix[index:index+1], matrix).flatten() # no normalization needed
	related_docs_indices = [i for i in sims.argsort()[::-1] if i != index]
	return [(index, sims[index]) for index in related_docs_indices][0:top_n]


for subreddit in subreddits:
	cols = ["Top {} Matches for {} with Raw TFs:".format(n, subreddit), "Cosine:", "Users:"]
	cols = cols + ["With Logged TFs:", "Cosine:", "Users:"]
	matches_raw = []
	scores_raw = []
	counts_raw = []
	matches_logged = []
	scores_logged = []
	counts_logged = []
	table = PrettyTable()
	subreddit_index = subredditlist.index(subreddit)
	for index, score in find_similar(tfidf_matrix_raw, subreddit_index, n):
		matches_raw.append(subredditlist[index])
		scores_raw.append("{:.2f}".format(score))
		counts_raw.append(user_counts[index])
	for index, score in find_similar(tfidf_matrix_logged, subreddit_index, n):
		matches_logged.append(subredditlist[index])
		scores_logged.append("{:.2f}".format(score))
		counts_logged.append()
	table.add_column(cols[0], matches_raw)
	table.add_column(cols[1], scores_raw)
	table.add_column(cols[2], counts_raw)
	table.add_column(cols[3], matches_logged)
	table.add_column(cols[4], scores_logged)
	table.add_column(cols[5], counts_logged)
	print(table)
	print("")
