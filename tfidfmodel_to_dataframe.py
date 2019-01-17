
import numpy as np
import pandas as pd
import pickle
import sys
from gensim.similarities import Similarity
from gensim.test.utils import get_tmpfile

fname = sys.argv[1]
vocabName = sys.argv[2]
subredditListFile = sys.argv[3]

model = pickle.load(open(fname, "rb"))
vocabulary = pickle.load(open(vocabName, "rb"))
subredditList = pickle.load(open(subredditListFile, "rb"))

index_tmp = get_tmpfile("index")
index = Similarity(index_tmp, model, num_features=len(vocabulary))
df = np.array(index)
del index
df = pd.DataFrame(df, index=subredditList, columns=subredditList)
