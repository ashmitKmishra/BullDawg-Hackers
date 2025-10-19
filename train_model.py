"""
ML Model Training for Benefit Recommendation System

Uses XGBoost for multi-label classification with 99%+ accuracy target.
Includes active learning for adaptive questioning.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, hamming_loss
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import json
from datetime import datetime
import os
from typing import Dict, List, Tuple

BENEFIT_TYPES = [
    'medical', 'dental', 'vision', 'life_insurance', 'disability',
    '401k', 'hsa', 'healthcare_fsa', 'dependent_care_fsa',
    'accident_insurance', 'critical_illness', 'hospital_indemnity',
    'legal_services', 'identity_theft', 'pet_insurance',
    'commuter_benefits', 'long_term_care', 'supplemental_life'
]


class BenefitMLModel:
    """XGBoost-based multi-label classifier for benefit recommendations"""
    
    def __init__(self):
        self.models = {}  # One model per benefit type
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.metrics = {}
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare and engineer features"""
        df = df.copy()
        
        # One-hot encode marital status if not already encoded
        if 'marital_status' in df.columns:
            df = pd.get_dummies(df, columns=['marital_status'], prefix='marital')
        
        # Ensure all expected columns exist
        for col in ['marital_single', 'marital_married', 'marital_divorced']:
            if col not in df.columns:
                df[col] = 0
        
        # Store feature columns for later
        if self.feature_columns is None:
            self.feature_columns = df.columns.tolist()
        
        return df
    
    def train(self, features_df: pd.DataFrame, labels_df: pd.DataFrame, 
              test_size=0.15, val_size=0.15):
        """
        Train one XGBoost model per benefit type
        
        Args:
            features_df: User features
            labels_df: Benefit selections (multi-label)
            test_size: Fraction for test set
            val_size: Fraction for validation set
        """
        print("=" * 70)
        print("TRAINING ML BENEFIT RECOMMENDATION MODEL")
        print("=" * 70)
        
        # Prepare features
        X = self.prepare_features(features_df)
        y = labels_df
        
        # Split data
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y['medical']
        )
        
        val_fraction = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_fraction, random_state=42
        )
        
        print(f"\nDataset split:")
        print(f"  Training:   {len(X_train):,} samples ({len(X_train)/len(X)*100:.1f}%)")
        print(f"  Validation: {len(X_val):,} samples ({len(X_val)/len(X)*100:.1f}%)")
        print(f"  Test:       {len(X_test):,} samples ({len(X_test)/len(X)*100:.1f}%)")
        
        # Scale features
        print(f"\nScaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train one model per benefit
        print(f"\nTraining {len(BENEFIT_TYPES)} XGBoost classifiers...")
        print("-" * 70)
        
        for i, benefit in enumerate(BENEFIT_TYPES, 1):
            print(f"[{i}/{len(BENEFIT_TYPES)}] Training model for: {benefit}")
            
            # Calculate class weight for imbalance
            pos_weight = (y_train[benefit] == 0).sum() / (y_train[benefit] == 1).sum()
            pos_weight = min(max(pos_weight, 0.5), 5.0)  # Clip between 0.5 and 5
            
            # XGBoost parameters OPTIMIZED for 99%+ accuracy
            params = {
                'objective': 'binary:logistic',
                'max_depth': 10,  # Increased from 8
                'learning_rate': 0.03,  # Decreased for better convergence
                'n_estimators': 700,  # Increased from 500
                'subsample': 0.9,  # Increased from 0.85
                'colsample_bytree': 0.9,  # Increased from 0.85
                'reg_alpha': 0.01,  # Decreased (less L1 regularization)
                'reg_lambda': 0.3,  # Decreased from 0.5
                'scale_pos_weight': pos_weight,  # Handle class imbalance
                'random_state': 42,
                'eval_metric': 'logloss',
                'early_stopping_rounds': 40,  # Increased from 30
                'min_child_weight': 1,
                'gamma': 0.05,  # Decreased
                'max_delta_step': 1  # Add for better handling of imbalanced classes
            }
            
            model = xgb.XGBClassifier(**params)
            
            # Train with early stopping
            model.fit(
                X_train_scaled, y_train[benefit],
                eval_set=[(X_val_scaled, y_val[benefit])],
                verbose=False
            )
            
            self.models[benefit] = model
            
            # Evaluate
            train_pred = model.predict(X_train_scaled)
            val_pred = model.predict(X_val_scaled)
            test_pred = model.predict(X_test_scaled)
            
            train_acc = accuracy_score(y_train[benefit], train_pred)
            val_acc = accuracy_score(y_val[benefit], val_pred)
            test_acc = accuracy_score(y_test[benefit], test_pred)
            
            test_prec = precision_score(y_test[benefit], test_pred, zero_division=0)
            test_rec = recall_score(y_test[benefit], test_pred, zero_division=0)
            test_f1 = f1_score(y_test[benefit], test_pred, zero_division=0)
            
            self.metrics[benefit] = {
                'train_accuracy': float(train_acc),
                'val_accuracy': float(val_acc),
                'test_accuracy': float(test_acc),
                'test_precision': float(test_prec),
                'test_recall': float(test_rec),
                'test_f1': float(test_f1),
                'prevalence': float(y_test[benefit].mean())
            }
            
            print(f"      Test Acc: {test_acc*100:.2f}% | Prec: {test_prec*100:.2f}% | Rec: {test_rec*100:.2f}% | F1: {test_f1:.3f}")
        
        # Overall metrics
        print("\n" + "=" * 70)
        print("OVERALL MODEL PERFORMANCE")
        print("=" * 70)
        
        # Make multi-label predictions
        y_pred_proba = self.predict_proba(X_test)
        y_pred = (y_pred_proba >= 0.5).astype(int)
        
        # Multi-label metrics
        hamming = hamming_loss(y_test, y_pred)
        exact_match = (y_test.values == y_pred).all(axis=1).mean()
        subset_accuracy = exact_match
        
        # Per-sample metrics
        sample_f1_scores = []
        for i in range(len(y_test)):
            if y_pred[i].sum() == 0 and y_test.iloc[i].sum() == 0:
                sample_f1_scores.append(1.0)
            elif y_pred[i].sum() == 0 or y_test.iloc[i].sum() == 0:
                sample_f1_scores.append(0.0)
            else:
                intersection = (y_pred[i] & y_test.iloc[i].values).sum()
                precision = intersection / y_pred[i].sum()
                recall = intersection / y_test.iloc[i].sum()
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                sample_f1_scores.append(f1)
        
        avg_f1 = np.mean(sample_f1_scores)
        
        print(f"\nMulti-Label Metrics:")
        print(f"  Hamming Loss:     {hamming:.4f} (lower is better)")
        print(f"  Exact Match:      {exact_match*100:.2f}% (all benefits correct)")
        print(f"  Subset Accuracy:  {subset_accuracy*100:.2f}%")
        print(f"  Average F1:       {avg_f1:.4f}")
        
        # Per-benefit average
        avg_test_acc = np.mean([m['test_accuracy'] for m in self.metrics.values()])
        avg_test_prec = np.mean([m['test_precision'] for m in self.metrics.values()])
        avg_test_rec = np.mean([m['test_recall'] for m in self.metrics.values()])
        
        print(f"\nPer-Benefit Averages:")
        print(f"  Accuracy:   {avg_test_acc*100:.2f}%")
        print(f"  Precision:  {avg_test_prec*100:.2f}%")
        print(f"  Recall:     {avg_test_rec*100:.2f}%")
        
        # Success check
        if avg_test_acc >= 0.99:
            print(f"\n✓ SUCCESS! Achieved 99%+ accuracy target!")
        else:
            print(f"\n⚠ Target not met. Current: {avg_test_acc*100:.2f}%")
        
        # Store for later
        self.metrics['overall'] = {
            'hamming_loss': float(hamming),
            'exact_match_ratio': float(exact_match),
            'subset_accuracy': float(subset_accuracy),
            'average_f1': float(avg_f1),
            'avg_accuracy': float(avg_test_acc),
            'avg_precision': float(avg_test_prec),
            'avg_recall': float(avg_test_rec)
        }
        
        print("\n" + "=" * 70)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict probabilities for all benefits"""
        X_prep = self.prepare_features(X)
        
        # Ensure all feature columns exist
        for col in self.feature_columns:
            if col not in X_prep.columns:
                X_prep[col] = 0
        X_prep = X_prep[self.feature_columns]
        
        X_scaled = self.scaler.transform(X_prep)
        
        predictions = np.zeros((len(X), len(BENEFIT_TYPES)))
        for i, benefit in enumerate(BENEFIT_TYPES):
            predictions[:, i] = self.models[benefit].predict_proba(X_scaled)[:, 1]
        
        return predictions
    
    def predict(self, X: pd.DataFrame, threshold=0.5) -> pd.DataFrame:
        """Predict benefit selections"""
        proba = self.predict_proba(X)
        predictions = (proba >= threshold).astype(int)
        return pd.DataFrame(predictions, columns=BENEFIT_TYPES, index=X.index)
    
    def get_uncertainties(self, X: pd.DataFrame) -> np.ndarray:
        """Get prediction uncertainties for active learning"""
        proba = self.predict_proba(X)
        # Uncertainty = distance from 0.5 (inverted)
        uncertainties = 1 - np.abs(proba - 0.5) * 2
        return uncertainties
    
    def save(self, filepath='models/benefit_model.pkl'):
        """Save model to disk"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'models': self.models,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'metrics': self.metrics,
            'benefit_types': BENEFIT_TYPES,
            'trained_at': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, filepath)
        print(f"\n✓ Model saved to: {filepath}")
        
        # Save metrics as JSON for easy reading
        metrics_path = filepath.replace('.pkl', '_metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"✓ Metrics saved to: {metrics_path}")
    
    @classmethod
    def load(cls, filepath='models/benefit_model.pkl'):
        """Load model from disk"""
        model_data = joblib.load(filepath)
        
        model = cls()
        model.models = model_data['models']
        model.scaler = model_data['scaler']
        model.feature_columns = model_data['feature_columns']
        model.metrics = model_data['metrics']
        
        print(f"✓ Model loaded from: {filepath}")
        print(f"  Trained: {model_data['trained_at']}")
        print(f"  Overall accuracy: {model.metrics['overall']['avg_accuracy']*100:.2f}%")
        
        return model


def main():
    """Train the ML model"""
    # Find latest training data
    data_files = sorted([f for f in os.listdir('data') if f.startswith('training_features')])
    if not data_files:
        print("ERROR: No training data found. Run generate_training_data.py first!")
        return
    
    latest_file = data_files[-1]
    # Extract full timestamp from filename: training_features_YYYYMMDD_HHMMSS.csv
    timestamp = '_'.join(latest_file.split('_')[2:]).replace('.csv', '')
    
    print(f"Loading training data: {latest_file}")
    features = pd.read_csv(f'data/training_features_{timestamp}.csv')
    labels = pd.read_csv(f'data/training_labels_{timestamp}.csv')
    
    # Train model
    model = BenefitMLModel()
    model.train(features, labels)
    
    # Save model
    model.save('models/benefit_model.pkl')
    
    print("\n" + "=" * 70)
    print("✓ Training complete! Model ready for deployment.")
    print("=" * 70)


if __name__ == '__main__':
    main()
