import gensim
import os
import pickle
import sys
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
import argparse


parser = argparse.ArgumentParser(description="Prepare tfidf and dictionary information for BoW similarity calculation")
parser.add_argument("read_dir", metavar='path', type=str)
parser.add_argument("fname_format", metavar='suffix', help="file name suffix for subreddit files to include. i.e. _2012_collapsed.txt")
parser.add_argument("content_or_users", choices=("content", "user"))
parser.add_argument("write_dir", metavar='path')
args = parser.parse_args()


def build_dictionary(readDir, fnameFormat):
    dictionary = Dictionary()
    for f in os.listdir(readDir):
        if f.lower().endswith(fnameFormat.lower()):
            with open("{}/{}".format(readDir, f), "r", errors="ignore") as reader:
                doc = reader.read().split()
                dictionary.add_documents([doc])
    dictionary.save("{}_dictionary{}_{}.p".format(readDir.replace("/",""), fnameFormat, content_or_users))
    return dictionary


def load_or_build_dictionary(readDir, fnameFormat, content_or_users):
    try:
        dictionary = Dictionary.load("{}_dictionary{}_{}.p".format(readDir.replace("/",""), fnameFormat, content_or_users))
        print("dictionary loaded from cache")
    except:
        dictionary = build_dictionary(readDir)
        print("created dictionary from scratch")
    return dictionary


def get_subreddits(readDir, fnameFormat, content_or_users):
    subreddits = []
    for f in os.listdir(readDir):
        if f.lower().endswith(fnameFormat.lower()):
            with open("{}/{}".format(readDir, f), "r") as reader:
                if content_or_users == "content":
                    subreddit = f.replace(fnameFormat, "")
                    subreddits.append(subreddit)
    return subreddits


def get_or_load_subreddits(readDir, fnameFormat, content_or_users):
    try:
        subreddits = [line.replace("\n", "") for line in open("subreddit_list_{}.txt".format(fnameFormat.replace(".txt", "")), "r").readlines()]
        print("subreddit list loaded from cache")
    except Exception as e:
        print(e)
        subreddits = get_subreddits(readDir, fnameFormat, content_or_users)
        print("created subreddit list from scratch")
        with open("subreddit_list_{}.txt".format(fnameFormat.replace(".txt", "")), "w") as writer:
            for sub in subreddits:
                writer.write(sub.replace("\n", "") + "\n")
    return subreddits


def read_corpus(readDir, subreddits, fnameFormat):
    for sr in subreddits:
        subreddit_path = "{}/{}{}".format(readDir, sr, fnameFormat)
        doc = open(subreddit_path, "r").read().split()
        yield dictionary.doc2bow(doc)


def gen_or_load_tfidf(dictionary, cache_path, smartirs):
    try:
        model = TfidfModel.load(cache_path)
        print("tfidfModel {} loaded from cache".format(cache_path))
    except:
        model = TfidfModel(dictionary=dictionary, normalize=False, smartirs=smartirs)
        model.save(cache_path)
        print("created tfidfModel {} from scratch".format(cache_path))
    return model


def cache_bow_features(dictionary, read_dir, write_dir, subreddits, fname_format):
    for sr in subreddits:
        subreddit_path = "{}/{}{}".format(read_dir, sr, fname_format)
        doc = open(subreddit_path, "r").read().split()
        bow = dictionary.doc2bow(doc)
        #write bow to write_dir/filename
        pickle.dump(bow, open("{}/{}.bow".format(writeDir, sr), "wb"))


dictionary = load_or_build_dictionary(args.read_dir, args.fname_format, args.content_or_users)
subreddits = get_or_load_subreddits(args.read_dir, args.fname_format, args.content_or_users)

cache_bow_features(dictionary, args.read_dir, args.write_dir, subreddits, args.fname_format)

tfidf_raw_cache_path = "{}/tfidf_model_raw_{}.p".format(args.write_dir, args.content_or_users)
tfidf_logged_cache_path = "{}/tfidf_model_logged_{}.p".format(args.write_dir, args.content_or_users)

tfidf_raw = gen_or_load_tfidf(dictionary, tfidf_raw_cache_path, smartirs="ntn")
tfidf_logged = gen_or_load_tfidf(dictionary, tfidf_logged_cache_path, smartirs="ltn")
