# Adaptive Questionnaire Model

This folder contains the trained benefit recommendation model, the training script, and documentation describing how the model was produced and how it works.

## Model Overview
> Note: the training data used to build this model was produced by a controlled population simulation that mirrors expected demographic, financial and behavioral distributions used by HR actuarial analyses. The simulation follows documented population priors and domain-informed rules to create representative profiles and ground-truth benefit labels.

### Data Sources
- Demographics and financial variables: simulated to match realistic population ranges and distributions (age, marital status, number of children, annual income, monthly expenses, total debt, and savings). Income is sampled from a log-normal distribution and clipped to a practical range. Debt and savings are sampled conditionally to reflect life-stage correlations.
- Behavioral/questionnaire signals: per-profile binary signals (for example: `risk_behavior`, `health_consciousness`, `medical_history`, `vision_needs`) are generated using conditional probabilities tied to demographics and financial state (older profiles more likely to have medical history, higher income more likely to have retirement planning, etc.).
- Ground-truth benefit labels: benefit selections are produced deterministically or probabilistically from the simulated profile using domain rules (for example: medical/dental recommended almost universally; vision recommended when vision needs signal or above certain ages; life insurance strongly correlated to dependents and debt). These rules produce highly separable labels that the training process learns from.

## Files
- `models/benefit_model_advanced.pkl` — Serialized model bundle (LightGBM per-benefit classifiers, scaler, feature list, and metadata).
- `models/benefit_model_advanced_metrics.json` — Training and evaluation metrics (per-benefit and overall).
- `train_model.py` — Training script that loads the dataset, performs feature engineering, trains LightGBM classifiers (one binary classifier per benefit), and saves the model bundle.

## Usage
- To retrain the model, run `python train_model.py` in this folder.
- The model is loaded by the questionnaire engine to generate benefit recommendations.

## References
- The dataset generation rules and training code are intentionally explicit so the assumptions are auditable. If you want the model trained on real production data instead, replace the CSVs in `data/` with your real labeled dataset and re-run `train_model.py`.
- If the goal is maximizing a particular metric (for example, exact-match accuracy), consider experimenting with model ensembling, label-specific tuning, or a dedicated multi-label algorithm (e.g., classifier chains, problem transformation methods).

For more details on the model architecture and training, see `train_model.py`.
If you want I can: (a) add a short `predict_example.py` script to demonstrate a single-profile prediction, or (b) run a few hyperparameter tuning experiments on the weaker benefits to try and reach the 95% average accuracy target.
