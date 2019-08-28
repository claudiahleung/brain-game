#ml folder for brain-game

Installing dependencies

Run from `brain-game/ml` directory in terminal
```bash
pip install requirements.txt
```

## Returning all data

Run from `brain-game` directory in Python console
```python
from ml.ml_scripts import analyze_data

training_data, labels = analyze_data.return_mu_data() # for mu data
training_data, labels = analyze_data.return_ssvep_data() # for ssvep data
```

## Running MinMaxScaler

Run from `brain-game` directory in terminal
```bash
python ml/ml_scripts/export_min_max_scaler.py
```

And pickled scalers should appear in `ml/saved_models/scalers`

Scalers can be loaded with
```python
from sklearn.externals import joblib
sc = joblib.load("filepath to scaler")
scaled_data = sc.transform(unscaled_data)
```