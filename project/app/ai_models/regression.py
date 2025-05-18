import numpy as np

class LinearRegression:
    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.weights = 0
        self.bias = 0

    def fit(self, X, y):
        n = len(X)
        for _ in range(self.epochs):
            y_pred = self.weights * X + self.bias
            dw = (-2/n) * sum(X * (y - y_pred))
            db = (-2/n) * sum(y - y_pred)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return self.weights * X + self.bias

