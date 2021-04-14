import xgboost as xgb
from xgboost import XGBClassifier
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier


data_path = r'C:\Users\User\coding\pythonProjects\TomatosProject\leaf_tagging\data'

columns = ['image', 'y'] + [f'x_{i}' for i in range(8)]
train_df = pd.read_csv(fr'{data_path}\LeavesDataTrain.csv', names=columns, header=None)
test_df = pd.read_csv(fr'{data_path}\LeavesDataTest.csv', names=columns, header=None)

y_train = train_df.iloc[:, 1]
x_train = train_df.iloc[:, 2:]

y_test = test_df.iloc[:, 1]
x_test = test_df.iloc[:, 2:]

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# model = XGBClassifier(use_label_encoder=False)
# model = RandomForestClassifier()
# model = SVC()
# model = DecisionTreeClassifier()
model = LogisticRegression()
# model = MLPClassifier()
print('Start fit')
model.fit(x_train, y_train)
print('Done fit')
pred = model.predict(x_test)
accuracy = accuracy_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)
mse = mean_squared_error(y_test, pred)
conf_matrix = confusion_matrix(y_test, pred)

print(f'Accuracy: {accuracy}')
print(f'MAE: {mae}')
print(f'MSE: {mse}')
print('confusion matrix:')
print(conf_matrix)
