import glob
import pickle
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

corpus = []
subredditList = []

dir_ = sys.argv[1]
for file in glob.glob("{}/*combined.txt".format(dir_)):
	with open(file, "r") as reader:
		subreddit = file.replace("{}/".format(dir_), "").replace("_combined.txt", "")
		corpus.append((subreddit, reader.read()))
		subredditList.append(subreddit)

tf_logged = TfidfVectorizer(analyzer="word", ngram_range=(1,1), min_df=0, stop_words=["[deleted]"], sublinear_tf=True)
tfidf_matrix_logged = tf_logged.fit_transform([content for file, content in corpus])

tf_raw = TfidfVectorizer(analyzer="word", ngram_range=(1,1), min_df=0, stop_words=["[deleted]"], sublinear_tf=False)
tfidf_matrix_logged = tf_raw.fit_transform([content for file, content in corpus])

pickle.dump(tfidf_matrix_logged, open("tfidf_matrix_logged.p", "wb"))
pickle.dump(tfidf_matrix_raw, open("tfidf_matrix_raw.p", "wb"))
pickle.dump(subredditList, open("subredditlist.p", "wb"))
