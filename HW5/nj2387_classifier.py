import sys
import string
import math

from collections import defaultdict


class NbClassifier(object):

    """
    A Naive Bayes classifier object has three parameters, all of which are populated during initialization:
    - a set of all possible attribute types
    - a dictionary of the probabilities P(Y), labels as keys and probabilities as values
    - a dictionary of the probabilities P(F|Y), with (feature, label) pairs as keys and probabilities as values
    """
    def __init__(self, training_filename, stopword_file):
        self.attribute_types = set()
        self.label_prior = {}    
        self.word_given_label = {}   

        self.collect_attribute_types(training_filename)
        if stopword_file is not None:
            self.remove_stopwords(stopword_file)
        self.train(training_filename)

    """
    A helper function to transform a string into a list of word strings.
    You should not need to modify this unless you want to improve your classifier in the extra credit portion.
    """
    def extract_words(self, text):
        no_punct_text = "".join([x for x in text.lower() if x not in string.punctuation])
        return [word for word in no_punct_text.split()]

    """
    Given a stopword_file, read in all stop words and remove them from self.attribute_types
    Implement this for extra credit.
    """
    def remove_stopwords(self, stopword_file):
        stopwords = set()
        with open(stopword_file) as file:
            lines = file.readlines()
            for line in lines:
                stopwords.add(line.strip())
        self.attribute_types.difference(stopwords)

    """
    Given a training datafile, add all features that appear at least m times to self.attribute_types
    """
    def collect_attribute_types(self, training_filename, m=1):
        extracted_features = defaultdict(int)

        with open(training_filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                msg = line.strip().split('\t')[1]
                words = self.extract_words(msg)
                for word in words:
                    extracted_features[word] += 1

        for word, count in extracted_features.items():
            if count >= m:
                self.attribute_types.add(word)

    """
    Given a training datafile, estimate the model probability parameters P(Y) and P(F|Y).
    Estimates should be smoothed using the smoothing parameter k.
    """
    def train(self, training_filename, k=0.1):

        word_given_label_count = defaultdict(int)
        label_info = defaultdict(int)
        label_pair_count = defaultdict(int)

        with open(training_filename, 'r') as file:
            lines = file.readlines()
            total_msgs = len(lines)
            for line in lines:
                label, msg = line.strip().split('\t')
                label_info[label] += 1

                words = self.extract_words(msg)
                label_pair_count[label] += len(words)
                for word in words:
                    word_given_label_count[tuple([word, label])] += 1

        labels = label_info.keys()

        for word in self.attribute_types:
            for label in labels:
                if (word, label) in word_given_label_count:
                    self.word_given_label[(word, label)] = (word_given_label_count[(word, label)] + k) / (
                            label_pair_count[label] + (k * len(self.attribute_types)))
                else:
                    self.word_given_label[(word, label)] = k / (label_pair_count[label] + (
                            k * len(self.attribute_types)))

        for label, count in label_info.items():
            self.label_prior[label] = count / total_msgs

    """
    Given a piece of text, return a relative belief distribution over all possible labels.
    The return value should be a dictionary with labels as keys and relative beliefs as values.
    The probabilities need not be normalized and may be expressed as log probabilities. 
    """
    def predict(self, text):

        predictions = {}
        words = self.extract_words(text)

        for label, prior_prob in self.label_prior.items():
            label_prob = math.log(prior_prob)
            sequence_prob = 0.0
            for word in words:
                if tuple([word, label]) in self.word_given_label.keys():
                    sequence_prob += math.log(self.word_given_label[tuple([word, label])])
            predictions[label] = label_prob + sequence_prob
        return predictions

    """
    Given a datafile, classify all lines using predict() and return the accuracy as the fraction classified correctly.
    """
    def evaluate(self, test_filename):
        correct_predictions = 0

        with open(test_filename, 'r') as file:
            lines = file.readlines()
            total_predictions = len(lines)
            for line in lines:
                label, msg = line.strip().split('\t')
                predictions = self.predict(msg)
                predicted_label = max(predictions, key=predictions.get)
                if predicted_label == label:
                    correct_predictions += 1
        return correct_predictions / total_predictions


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("\nusage: ./hmm.py [training data file] [test or dev data file] [(optional) stopword file]")
        exit(0)
    elif len(sys.argv) == 3:
        classifier = NbClassifier(sys.argv[1], None)
    else:
        classifier = NbClassifier(sys.argv[1], sys.argv[3])
    print(classifier.evaluate(sys.argv[2]))
