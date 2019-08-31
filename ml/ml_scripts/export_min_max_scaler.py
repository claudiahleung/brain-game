import analyze_data
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib

mu_data, _ = analyze_data.return_mu_data()

mu_norm_model = MinMaxScaler()
_ = mu_norm_model.fit_transform(mu_data)
joblib.dump(mu_norm_model, "ml/saved_models/scaler/mu_overall_min_max_scaler.pkl")

ssvep_data, _ = analyze_data.return_ssvep_data()

ssvep_norm_model = MinMaxScaler()
_ = ssvep_norm_model.fit_transform(ssvep_data)
joblib.dump(ssvep_norm_model, "ml/saved_models/scaler/ssvep_overall_min_max_scaler.pkl")
