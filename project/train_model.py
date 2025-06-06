# train_model.py
import csv
import numpy as np
from app.ai_models.regression import LinearRegressionCustom
import joblib

def load_data(filepath):
    hours = []
    scores = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hours.append(float(row['Hours']))
            scores.append(float(row['Score']))
    return np.array(hours), np.array(scores)

def train_and_save():
    X, y = load_data('instance/student_scores.csv')
    model = LinearRegressionCustom()
    model.fit(X, y)
    print(f"Model trained. Coef: {model.coefficient}, Intercept: {model.intercept}")
    joblib.dump(model, 'instance/model.pkl')

if __name__ == '__main__':
    train_and_save()
