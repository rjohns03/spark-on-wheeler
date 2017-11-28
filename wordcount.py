from __future__ import print_function
import time, re, sys
from pyspark import SparkContext, SparkConf

def linesToWordsFunc(line):
    wordsList = line.split()
    wordsList = [re.sub(r'\W+', '', word) for word in wordsList]
    filtered = filter(lambda word: re.match(r'\w+', word), wordsList)
    return filtered

def wordsToPairsFunc(word):
    return (word, 1)

def reduceToCount(a, b):
    return (a + b)

def main():
    conf = SparkConf().setAppName("Words count").setMaster("local")
    sc = SparkContext(conf=conf)
    rdd = sc.textFile(sys.argv[1])

    words = rdd.flatMap(linesToWordsFunc)
    pairs = words.map(wordsToPairsFunc)
    counts = pairs.reduceByKey(reduceToCount)

    # Get the first top 100 words
    output = counts.takeOrdered(100, lambda (k, v): -v)

    for(word, count) in output:
        print(word + ': ' + str(count))

    sc.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: wordcount <file>", file=sys.stderr)
        exit(-1)
    main()
