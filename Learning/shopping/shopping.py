import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            temp_evidence = list()
            temp_evidence.extend([int(row[0]), float(row[1]), int(row[2]), float(row[3]), int(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9])])

            if row[10] == 'Jan':
                temp_evidence.append(0)
            elif row[10] == 'Feb':
                temp_evidence.append(1)
            elif row[10] == 'Mar':
                temp_evidence.append(2)
            elif row[10] == 'Apr':
                temp_evidence.append(3)
            elif row[10] == 'May':
                temp_evidence.append(4)
            elif row[10] == 'June':
                temp_evidence.append(5)
            elif row[10] == 'Jul':
                temp_evidence.append(6)
            elif row[10] == 'Aug':
                temp_evidence.append(7)
            elif row[10] == 'Sep':
                temp_evidence.append(8)
            elif row[10] == 'Oct':
                temp_evidence.append(9)
            elif row[10] == 'Nov':
                temp_evidence.append(10)
            elif row[10] == 'Dec':
                temp_evidence.append(11)
            else:
                temp_evidence.append(0)

            temp_evidence.extend([int(row[11]), int(row[12]), int(row[13]), int(row[14])])

            temp_evidence.append(1 if row[15] == 'Returning_Visitor' else 0)
            temp_evidence.append(0 if row[16] == 'FALSE' else 1)
            
            evidence.append(temp_evidence)
            labels.append(0 if row[17] == 'FALSE' else 1)

    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0

    num_positive = sum(labels)
    num_negative = len(labels) - num_positive

    num_true_positive = 0
    num_true_negative = 0
    for i in range(len(predictions)):
        if predictions[i] == 1 and predictions[i] == labels[i]:
            num_true_positive += 1
        elif predictions[i] == 0 and predictions[i] == labels[i]:
            num_true_negative += 1
    
    sensitivity = num_true_positive/num_positive
    specificity = num_true_negative/num_negative

    return(sensitivity, specificity)


if __name__ == "__main__":
    main()
