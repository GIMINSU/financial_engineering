from feature_selector import FeatureSelector
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

import pandas as pd

cancer = load_breast_cancer()
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
# print(df.head())
df_label = list(df)
# X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=42)
# print(cancer)
# print(X_test)

fs = FeatureSelector(data = df, labels= df_label)

fs.identify_missing(missing_threshold=0.5)
missing_features = fs.ops['missing']
print(missing_features)

fs.identify_single_unique()
single_unique = fs.ops['single_unique']
print(single_unique)

fs.identify_collinear(correlation_threshold=0.975)
correlated_feature = fs.ops['collinear']
print(correlated_feature[:])
# fs.plot_collinear()
fs.plot_collinear(plot_all=True)
fs.identify_collinear(correlation_threshold=0.98)

print(fs.record_collinear.head())
print(fs.identify_zero_importance(task='classification', eval_metric='auc', n_iterations=10, early_stopping=True))
plt.show()