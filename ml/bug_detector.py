import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from typing import List, Dict, Any
import pickle
import os

class BugDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.bug_types = [
            'memory_leak', 'buffer_overflow', 'null_pointer',
            'uninitialized_var', 'infinite_loop', 'missing_return',
            'syntax_error'
        ]

    def train(self, code_samples: List[Dict[str, Any]], epochs: int = 10):
        """Train the model on code samples"""
        # Prepare training data
        X = self.vectorizer.fit_transform([sample['code_content'] for sample in code_samples])
        y = np.zeros((len(code_samples), len(self.bug_types)))
        
        for i, sample in enumerate(code_samples):
            for bug in sample.get('bugs', []):
                if bug['bug_type'] in self.bug_types:
                    y[i, self.bug_types.index(bug['bug_type'])] = 1

        # Train the model
        self.model.fit(X.toarray(), y)

    def predict(self, code: str) -> List[Dict[str, Any]]:
        """Predict potential bugs in code"""
        # Vectorize the input code
        X = self.vectorizer.transform([code])
        
        # Get predictions
        predictions = self.model.predict(X.toarray())[0]
        probabilities = self.model.predict_proba(X.toarray())[0]
        
        # Convert predictions to bug reports
        bugs = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            if pred > 0:  # If the model predicts this bug type
                bugs.append({
                    'bug_type': self.bug_types[i],
                    'confidence': float(prob[1]),  # Probability of positive class
                    'description': f'Potential {self.bug_types[i]} detected'
                })
        
        return bugs

    def save_model(self, model_path: str = 'models/bug_detector'):
        """Save the trained model and vectorizer"""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(f'{model_path}_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        with open(f'{model_path}_vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)

    def load_model(self, model_path: str = 'models/bug_detector'):
        """Load a trained model and vectorizer"""
        with open(f'{model_path}_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open(f'{model_path}_vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f) 