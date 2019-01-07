import glob
import pickle
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = []
subredditList = []

dir_ = sys.argv[1]
fnameFormatting = sys.argv[2]
pickleFlag = sys.argv[3]

for file in glob.glob("{}/*{}.txt".format(dir_, fnameFormatting)):
	with open(file, "r") as reader:
		subreddit = file.replace("{}/".format(dir_), "").replace("_combined.txt", "")
		corpus.append((subreddit, reader.read()))
		subredditList.append(subreddit)

cv = CountVectorizer()
tdm = cv.fit_transform([content for file, content in corpus])

user_counts = tdm.toarray().astype(bool).sum(axis=1)
assert len(subredditList) == len(user_counts)

del cv, tdm

# NON-NORMALIZED -- will not work with sklearn.metrics.pairwise.linear_kernel()
tf_raw = TfidfVectorizer(norm=None, analyzer="word", ngram_range=(1,1), stop_words=["[deleted]"], sublinear_tf=False)
tfidf_matrix_raw = tf_raw.fit_transform([content for file, content in corpus])
assert len(subredditList) == tfidf_matrix_raw.shape[0]

# NON-NORMALIZED -- will not work with sklearn.metrics.pairwise.linear_kernel()
tf_logged = TfidfVectorizer(norm=None, analyzer="word", ngram_range=(1,1), stop_words=["[deleted]"], sublinear_tf=True)
tfidf_matrix_logged = tf_logged.fit_transform([content for file, content in corpus])
assert len(subredditList) == tfidf_matrix_logged.shape[0]

pickle.dump(subredditList, open("{}_subredditlist.p".format(pickleFlag), "wb"))
pickle.dump(user_counts, open("{}_user_counts.p".format(pickleFlag), "wb"))
pickle.dump(tfidf_matrix_raw, open("{}_tfidf_matrix_raw.p".format(pickleFlag), "wb"))
pickle.dump(tfidf_matrix_logged, open("{}_tfidf_matrix_logged.p".format(pickleFlag), "wb"))
