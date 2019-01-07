import pickle
import sys
from prettytable import PrettyTable
from sklearn.metrics.pairwise import linear_kernel

try:
	assert len(sys.argv) >= 4
except:
	print("Usage: python find_similar.py directory subreddit subreddit...subreddit num_matches")

tfidf_matrix_logged = pickle.load(open("tfidf_matrix_logged.p", "rb"))
tfidf_matrix_raw = pickle.load(open("tfidf_matrix_raw.p", "rb"))

def find_similar(matrix, index, top_n):
	sims = linear_kernel(matrix[index:index+1], matrix).fatten()
	related_docs_indices = [i for i in sims.argsort()[::-1] if i != index]
	return [(index, sims[index]) for index in related_docs_indices][0:top_n]
	
dir_ = sys.argv[1]
subreddits = sys.argv[2:-1]
n = int(sys.argv[-1])

all = [tup[0] for tup in tfidf

for subreddit in subreddits:
	
