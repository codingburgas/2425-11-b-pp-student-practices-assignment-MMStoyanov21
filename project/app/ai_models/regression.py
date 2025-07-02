"""
Module: regression.py
Description: Implements a basic Linear Regression model using gradient descent.
"""

import numpy as np

class LinearRegression:
    """
    A simple implementation of linear regression for univariate data.
    """

    def __init__(self, lr=0.01, epochs=1000):
        """
        Initialize the model with learning rate and training epochs.

        Args:
            lr (float): Learning rate for gradient descent.
            epochs (int): Number of iterations for training.
        """
        self.lr = lr
        self.epochs = epochs
        self.weights = 0.0
        self.bias = 0.0

    def fit(self, X, y):
        """
        Train the model on the given data using gradient descent.

        Args:
            X (array-like): Input feature values.
            y (array-like): Target values to predict.
        """
        n = len(X)
        for _ in range(self.epochs):
            y_pred = self.weights * X + self.bias
            dw = (-2/n) * np.sum(X * (y - y_pred))
            db = (-2/n) * np.sum(y - y_pred)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        """
        Predict target values for the provided input.

        Args:
            X (array-like): Input feature values.

        Returns:
            array-like: Predicted target values.
        """
        return self.weights * X + self.bias
