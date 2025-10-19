"""
Advanced ML Model Training with LightGBM + Feature Engineering
Target: 95%+ accuracy
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
import joblib
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Define all benefit types
BENEFIT_TYPES = [
    'medical', 'dental', 'vision', 'life_insurance', 'disability',
    '401k', 'hsa', 'healthcare_fsa', 'dependent_care_fsa',
    'accident_insurance', 'critical_illness', 'hospital_indemnity',
    'legal_services', 'identity_theft', 'pet_insurance',
    'commuter_benefits', 'long_term_care', 'supplemental_life'
]


class AdvancedBenefitMLModel:
    """
    Advanced multi-label benefit recommendation model using LightGBM
    with sophisticated feature engineering
    """
    
    def __init__(self):
        self.models: Dict[str, lgb.Booster] = {}
        self.scaler = StandardScaler()
        self.feature_names: List[str] = []
        self.metrics: Dict = {}
        
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Advanced feature engineering to extract maximum signal
        """
        df = df.copy()
        
        # Age-based features
        df['age_group'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 100], labels=['young', 'middle', 'senior', 'elder', 'retired'])
        df['is_retirement_age'] = (df['age'] >= 55).astype(int)
        df['is_young_adult'] = (df['age'] <= 30).astype(int)
        df['age_squared'] = df['age'] ** 2
        
        # Income-based features
        df['income_bracket'] = pd.cut(df['annual_income'], 
                                       bins=[0, 50000, 75000, 100000, 150000, 1000000],
                                       labels=['low', 'medium', 'high', 'very_high', 'wealthy'])
        df['log_income'] = np.log1p(df['annual_income'])
        df['income_per_family_member'] = df['annual_income'] / (df['num_children'] + 1 + df['is_married'])
        
        # Financial health features
        df['debt_to_income_ratio'] = df['total_debt'] / (df['annual_income'] + 1)
        df['savings_rate'] = df['savings'] / (df['annual_income'] + 1)
        df['net_worth'] = df['savings'] - df['total_debt']
        df['financial_stress'] = ((df['debt_to_income_ratio'] > 0.5).astype(int) * 2 + 
                                   (df['savings_rate'] < 0.1).astype(int))
        df['high_debt_flag'] = (df['total_debt'] > 100000).astype(int)
        df['low_savings_flag'] = (df['savings'] < 10000).astype(int)
        
        # Family features
        df['has_children'] = (df['num_children'] > 0).astype(int)
        df['is_married'] = (df['marital_status'] == 'married').astype(int)
        df['family_size'] = df['num_children'] + 1 + df['is_married']
        df['large_family'] = (df['family_size'] >= 4).astype(int)
        df['single_parent'] = ((df['marital_status'] != 'married') & (df['num_children'] > 0)).astype(int)
        
        # Health risk features
        df['health_risk_score'] = (df['medical_history'] + df['chronic_conditions'] + 
                                    df['hospital_visits'] + df['cancer_history'] + df['heart_health'])
        df['high_health_risk'] = (df['health_risk_score'] >= 3).astype(int)
        df['preventive_care_score'] = df['health_consciousness'] + df['dental_habits'] + df['exercise_frequency']
        
        # Work-life features
        df['work_risk_score'] = df['hazardous_job'] + df['risk_behavior'] + df['driving_habits']
        df['commutes'] = (df['commute'] == 1) & (df['work_from_home'] == 0)
        
        # Age-income interactions (critical for benefit prediction)
        df['age_x_income'] = df['age'] * df['log_income']
        df['age_x_debt'] = df['age'] * df['debt_to_income_ratio']
        df['age_x_health_risk'] = df['age'] * df['health_risk_score']
        
        # Income-family interactions
        df['income_x_children'] = df['log_income'] * df['num_children']
        df['income_x_married'] = df['log_income'] * df['is_married']
        
        # Health-age interactions
        df['health_x_age_50plus'] = df['health_risk_score'] * (df['age'] > 50).astype(int)
        
        # Benefit-specific signals
        df['vision_signal'] = df['vision_needs'] + (df['age'] > 40).astype(int)
        df['retirement_signal'] = df['retirement_planning'] + (df['age'] > 35).astype(int) + (df['annual_income'] > 60000).astype(int)
        df['fsa_signal'] = df['medical_history'] + df['chronic_conditions'] + df['hospital_visits']
        df['critical_illness_signal'] = df['chronic_conditions'] + df['cancer_history'] + df['heart_health'] + (df['age'] > 50).astype(int)
        df['disability_signal'] = df['hazardous_job'] + (df['total_debt'] > 50000).astype(int) + df['has_children']
        df['life_insurance_signal'] = df['has_children'] + df['is_married'] + (df['total_debt'] > 100000).astype(int)
        
        # Polynomial features for key signals
        df['vision_signal_squared'] = df['vision_signal'] ** 2
        df['retirement_signal_squared'] = df['retirement_signal'] ** 2
        df['health_risk_squared'] = df['health_risk_score'] ** 2
        
        # One-hot encode categorical features
        df = pd.get_dummies(df, columns=['marital_status', 'age_group', 'income_bracket'], drop_first=False)
        
        return df
    
    def prepare_features(self, df: pd.DataFrame, fit_scaler: bool = False) -> pd.DataFrame:
        """
        Prepare features with engineering and scaling
        """
        # Engineer features
        df = self._engineer_features(df)
        
        # Get numeric columns only
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if fit_scaler:
            df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
            self.feature_names = df.columns.tolist()
        else:
            # Ensure all expected columns exist
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0
            df = df[self.feature_names]
            df[numeric_cols] = self.scaler.transform(df[numeric_cols])
        
        return df
    
    def train(self, features_df: pd.DataFrame, labels_df: pd.DataFrame, 
              test_size: float = 0.15, val_size: float = 0.15):
        """
        Train LightGBM models with advanced parameters for 95%+ accuracy
        """
        print("="*70)
        print("ADVANCED ML TRAINING - TARGET: 95%+ ACCURACY")
        print("="*70)
        
        # Split data
        X_temp, X_test, y_temp, y_test = train_test_split(
            features_df, labels_df, test_size=test_size, random_state=42, stratify=None
        )
        
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=42, stratify=None
        )
        
        print(f"\nDataset split:")
        print(f"  Training:   {len(X_train):,} samples ({len(X_train)/len(features_df)*100:.1f}%)")
        print(f"  Validation: {len(X_val):,} samples ({len(X_val)/len(features_df)*100:.1f}%)")
        print(f"  Test:       {len(X_test):,} samples ({len(X_test)/len(features_df)*100:.1f}%)")
        
        # Feature engineering and scaling
        print("\nEngineering features...")
        X_train = self.prepare_features(X_train, fit_scaler=True)
        X_val = self.prepare_features(X_val, fit_scaler=False)
        X_test = self.prepare_features(X_test, fit_scaler=False)
        
        print(f"Feature engineering complete: {len(self.feature_names)} features")
        
        # Train models
        print(f"\nTraining {len(BENEFIT_TYPES)} LightGBM classifiers...")
        print("-"*70)
        
        all_metrics = []
        
        for i, benefit in enumerate(BENEFIT_TYPES, 1):
            print(f"[{i}/{len(BENEFIT_TYPES)}] Training model for: {benefit}")
            
            # Calculate class weight
            pos_count = y_train[benefit].sum()
            neg_count = len(y_train) - pos_count
            scale_pos_weight = neg_count / pos_count if pos_count > 0 else 1.0
            scale_pos_weight = min(max(scale_pos_weight, 0.5), 10.0)  # Clip
            
            # LightGBM parameters optimized for high accuracy - ULTRA AGGRESSIVE
            params = {
                'objective': 'binary',
                'metric': 'binary_logloss',
                'boosting_type': 'gbdt',
                'num_leaves': 255,
                'max_depth': 15,
                'learning_rate': 0.01,
                'n_estimators': 2000,
                'subsample': 0.95,
                'colsample_bytree': 0.95,
                'reg_alpha': 0.001,
                'reg_lambda': 0.1,
                'min_child_samples': 5,
                'scale_pos_weight': scale_pos_weight,
                'random_state': 42,
                'verbose': -1,
                'min_split_gain': 0.0001,
                'min_child_weight': 0.0001,
                'feature_fraction': 0.98,
                'bagging_fraction': 0.98,
                'bagging_freq': 1,
                'lambda_l1': 0.001,
                'lambda_l2': 0.1,
                'max_bin': 511,
                'num_threads': -1,
                'force_row_wise': True
            }
            
            # Create datasets
            train_data = lgb.Dataset(X_train, label=y_train[benefit])
            val_data = lgb.Dataset(X_val, label=y_val[benefit], reference=train_data)
            
            # Train with early stopping
            model = lgb.train(
                params,
                train_data,
                valid_sets=[train_data, val_data],
                valid_names=['train', 'val'],
                callbacks=[
                    lgb.early_stopping(stopping_rounds=50, verbose=False),
                    lgb.log_evaluation(period=0)
                ]
            )
            
            self.models[benefit] = model
            
            # Evaluate
            y_pred_proba = model.predict(X_test)
            y_pred = (y_pred_proba >= 0.5).astype(int)
            y_true = y_test[benefit].values
            
            # Calculate metrics
            tp = ((y_pred == 1) & (y_true == 1)).sum()
            tn = ((y_pred == 0) & (y_true == 0)).sum()
            fp = ((y_pred == 1) & (y_true == 0)).sum()
            fn = ((y_pred == 0) & (y_true == 1)).sum()
            
            accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            metrics = {
                'benefit': benefit,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'best_iteration': model.best_iteration
            }
            all_metrics.append(metrics)
            
            print(f"      Test Acc: {accuracy*100:.2f}% | Prec: {precision*100:.2f}% | "
                  f"Rec: {recall*100:.2f}% | F1: {f1:.3f} | Trees: {model.best_iteration}")
        
        # Calculate overall metrics
        print("\n" + "="*70)
        print("OVERALL MODEL PERFORMANCE")
        print("="*70)
        
        # Multi-label metrics
        y_pred_all = np.zeros_like(y_test.values)
        for i, benefit in enumerate(BENEFIT_TYPES):
            y_pred_proba = self.models[benefit].predict(X_test)
            y_pred_all[:, i] = (y_pred_proba >= 0.5).astype(int)
        
        hamming_loss = (y_pred_all != y_test.values).sum() / y_test.size
        exact_match = (y_pred_all == y_test.values).all(axis=1).mean()
        
        avg_accuracy = np.mean([m['accuracy'] for m in all_metrics])
        avg_precision = np.mean([m['precision'] for m in all_metrics])
        avg_recall = np.mean([m['recall'] for m in all_metrics])
        avg_f1 = np.mean([m['f1'] for m in all_metrics])
        
        print(f"\nMulti-Label Metrics:")
        print(f"  Hamming Loss:     {hamming_loss:.4f} (lower is better)")
        print(f"  Exact Match:      {exact_match*100:.2f}% (all benefits correct)")
        print(f"  Subset Accuracy:  {exact_match*100:.2f}%")
        print(f"  Average F1:       {avg_f1:.4f}")
        
        print(f"\nPer-Benefit Averages:")
        print(f"  Accuracy:   {avg_accuracy*100:.2f}%")
        print(f"  Precision:  {avg_precision*100:.2f}%")
        print(f"  Recall:     {avg_recall*100:.2f}%")
        
        # Check target
        if avg_accuracy >= 0.95:
            print(f"\n🎉 TARGET ACHIEVED! Accuracy: {avg_accuracy*100:.2f}% >= 95%")
        else:
            print(f"\n⚠ Target not met. Current: {avg_accuracy*100:.2f}% (Need: 95.00%)")
            gap = 95.0 - avg_accuracy*100
            print(f"   Gap to target: {gap:.2f} percentage points")
        
        print("\n" + "="*70)
        
        self.metrics = {
            'per_benefit': all_metrics,
            'overall': {
                'accuracy': avg_accuracy,
                'precision': avg_precision,
                'recall': avg_recall,
                'f1': avg_f1,
                'hamming_loss': hamming_loss,
                'exact_match': exact_match
            }
        }
        
        return self.metrics
    
    def predict_proba(self, features_df: pd.DataFrame) -> Dict[str, float]:
        """
        Predict probability for each benefit
        """
        X = self.prepare_features(features_df, fit_scaler=False)
        
        predictions = {}
        for benefit in BENEFIT_TYPES:
            if benefit in self.models:
                pred = self.models[benefit].predict(X)[0]
                predictions[benefit] = float(pred)
        
        return predictions
    
    def predict(self, features_df: pd.DataFrame, threshold: float = 0.5) -> Dict[str, int]:
        """
        Predict binary recommendations for each benefit
        """
        proba = self.predict_proba(features_df)
        return {benefit: 1 if prob >= threshold else 0 
                for benefit, prob in proba.items()}
    
    def save(self, model_path: str = 'models/benefit_model_advanced.pkl'):
        """
        Save model, scaler, and metadata
        """
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'models': self.models,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'metrics': self.metrics,
            'benefit_types': BENEFIT_TYPES
        }
        
        joblib.dump(model_data, model_path)
        print(f"✓ Model saved to: {model_path}")
        
        # Save metrics separately
        metrics_path = model_path.replace('.pkl', '_metrics.json')
        with open(metrics_path, 'w') as f:
            # Convert numpy types to native Python types for JSON
            metrics_json = {
                'per_benefit': [
                    {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                     for k, v in m.items()} 
                    for m in self.metrics['per_benefit']
                ],
                'overall': {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                           for k, v in self.metrics['overall'].items()}
            }
            json.dump(metrics_json, f, indent=2)
        print(f"✓ Metrics saved to: {metrics_path}")
    
    def load(self, model_path: str = 'models/benefit_model_advanced.pkl'):
        """
        Load model, scaler, and metadata
        """
        model_data = joblib.load(model_path)
        self.models = model_data['models']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.metrics = model_data.get('metrics', {})
        print(f"✓ Model loaded from: {model_path}")


def main():
    """
    Main training function
    """
    # Find latest training data
    data_dir = Path('data')
    feature_files = sorted(data_dir.glob('training_features_*.csv'))
    
    if not feature_files:
        print("❌ Error: No training data found in data/ directory")
        print("   Please run generate_training_data.py first")
        return
    
    latest_features = feature_files[-1]
    timestamp = latest_features.stem.split('_', 2)[2]
    latest_labels = data_dir / f'training_labels_{timestamp}.csv'
    
    if not latest_labels.exists():
        print(f"❌ Error: Labels file not found: {latest_labels}")
        return
    
    print(f"Loading training data: {latest_features.name}")
    
    # Load data
    features = pd.read_csv(latest_features)
    labels = pd.read_csv(latest_labels)
    
    # Train model
    model = AdvancedBenefitMLModel()
    metrics = model.train(features, labels, test_size=0.15, val_size=0.15)
    
    # Save model
    model.save('models/benefit_model_advanced.pkl')
    
    print("\n" + "="*70)
    print("✓ Training complete! Model ready for deployment.")
    print("="*70)


if __name__ == '__main__':
    main()
