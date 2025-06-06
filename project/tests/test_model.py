# tests/test_model.py
import unittest
import numpy as np
from app.ai_models.regression import LinearRegressionCustom

class TestModel(unittest.TestCase):
    def test_fit_predict(self):
        X = np.array([1, 2, 3])
        y = np.array([2, 4, 6])
        model = LinearRegressionCustom()
        model.fit(X, y, epochs=1000, lr=0.01)
        y_pred = model.predict([4])
        self.assertAlmostEqual(y_pred[0], 8, delta=0.5)

if __name__ == '__main__':
    unittest.main()
