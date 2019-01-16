import gensim
import os
import pickle
import sys
from gensim.corpora import Dictionary
from gensim.models import TfidfModel

assert len(sys.argv) == 8
assert sys.argv[4] in ["content", "users", "user"]

readDir = sys.argv[1]
fnameFormat = sys.argv[2]
pickleFlag = sys.argv[3]
content_or_users = sys.argv[4]
if content_or_users == "user":
	content_or_users = "users"
writeDir = sys.argv[5]
query = sys.argv[6]
num_matches = int(sys.argv[7]) + 1

subredditList = []

try:
    vocabulary = pickle.load(open("{}/vocabulary{}.p".format(readDir, fnameFormat), "rb"))
except:
    vocabulary = set()
    for f in os.listdir(readDir):
        if fnameFormat.lower() in f.lower():
            with open("{}/{}".format(readDir, f), "r", errors="ignore") as reader:
                doc = set(reader.read().split())
                for word in doc:
                    vocabulary.add(word)
    pickle.dump(vocabulary, open("{}/vocabulary{}.p".format(readDir, fnameFormat), "wb"))

dictionary = Dictionary([list(vocabulary)])


class MyCorpus(object):
    def __iter__(self):
        for f in os.listdir(readDir):
            if fnameFormat.lower() in f.lower():
                with open("{}/{}".format(readDir, f), "r", errors="ignore") as reader:
                    subreddit = f.split("-")[0]
                    subredditList.append(subreddit)
                    yield dictionary.doc2bow(reader.read().lower().split())


corpus = MyCorpus()

tfidf_raw = TfidfModel(corpus, normalize=False, smartirs="ntn")
tfidf_logged = TfidfModel(corpus, normalize=False, smartirs="ltn")

raw_sims = gensim.similarities.Similarity(writeDir,tfidf_raw[corpus],
                                        num_features=len(vocabulary))
logged_sims = gensim.similarities.Similarity(writeDir, tfidf_logged[corpus],
                                        num_features=len(vocabulary))

pickle.dump(raw_sims, open("{}/{}_tfidf_raw_sims_{}.p".format(writeDir, pickleFlag, content_or_users), "wb"))
pickle.dump(logged_sims, open("{}/{}_tfidf_logged_sims_{}.p".format(writeDir, pickleFlag, content_or_users), "wb"))

queryVector = open("{}/{}{}".format(readDir, query, fnameFormat)).read().lower().split()
queryVector = dictionary.doc2bow(queryVector)
raw_tfidf_query = tfidf_raw[queryVector]
logged_tfidf_query = tfidf_logged[queryVector]

x = list(enumerate(raw_sims[raw_tfidf_query]))
x.sort(key=lambda x: x[1], reverse=True)
x = x[:num_matches]
x = [(subredditList[match[0]], match[1]) for match in x]
y = list(enumerate(logged_sims[logged_tfidf_query]))
y.sort(key=lambda x: x[1], reverse=True)
y = y[:num_matches]
y = [(subredditList[match[0]], match[1]) for match in y]

print("Top {} Matches Using Raw Term Frequences:".format(num_matches))
for match in x:
    print("{} ({:.2f})".format(match[0], match[1]))
print("\n")
print("Top {} Matches Using Logged Term Frequences:".format(num_matches))
for match in y:
    print("{} ({:.2f})".format(match[0], match[1]))








#
