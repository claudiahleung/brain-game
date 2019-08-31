import analyze_data
from sklearn.preprocessing import Normalizer
from sklearn.externals import joblib

mu_data, _ = analyze_data.return_mu_data()

mu_norm_model = Normalizer()
print(mu_data.shape)
_ = mu_norm_model.fit_transform(mu_data)
joblib.dump(mu_norm_model, "ml/saved_models/normalizer/mu_overall_normalizer.pkl")

ssvep_data, _ = analyze_data.return_ssvep_data()

ssvep_norm_model = Normalizer()
print(ssvep_data.shape)
_ = ssvep_norm_model.fit_transform(ssvep_data)
joblib.dump(ssvep_norm_model, "ml/saved_models/normalizer/ssvep_overall_normalizer.pkl")
