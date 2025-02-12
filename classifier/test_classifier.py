import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.cross_validation import train_test_split

from preprocessing.preprocess import get_preprocessed_data as get_data, balance_samples

# NROWS = 2000
# import some test data
ds = datasets.load_iris()
X, Y = ds.data, ds.target

X, Y = get_data("diabetic_data_initial.csv")
# delete one of the columns which causes trouble with small data sets

# I guess we can keep this on hand to test trees or other classifiers that need categorical variables
categorical_X, categorical_Y = get_data("diabetic_data_initial.csv", unfold=False)

#X, Y = balance_samples(X, Y)
#X, Y = pd.DataFrame(X), pd.DataFrame(Y)

def test_classifier_accuracy(classifier, folds=10, num_samples=None, unfold=True):
    acc = []
    temp_X, temp_Y = X, Y
    if not unfold:
        temp_X, temp_Y = categorical_X, categorical_Y

    for i in range(folds):
        train_X, test_X, train_Y, test_Y = train_test_split(
            temp_X.values, temp_Y.values, train_size=num_samples, test_size=num_samples/2)

        classifier.train(train_X, train_Y)
        acc.append(classifier.accuracy(*balance_samples(test_X, test_Y)))

        print "Fold #{fold}: {accuracy:2.2f}% accuracy".format(fold=i, accuracy=acc[-1]*100)

    return np.mean(acc)

def test_classifier(classifier, **kwargs):
    print "{classifier} achieved {accuracy:2.2f}% accuracy".format(
        classifier=classifier,
        accuracy=100 * test_classifier_accuracy(classifier, **kwargs))

# inject your own data
def _test_classifier_accuracy(classifier, train_X, train_Y, test_X, test_Y):
    classifier.train(train_X, train_Y)
    return classifier.accuracy(test_X, test_Y)
