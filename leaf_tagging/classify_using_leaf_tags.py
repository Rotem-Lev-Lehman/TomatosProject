import numpy as np
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
from sklearn.model_selection import cross_val_score


data_path = r'C:\Users\User\coding\pythonProjects\TomatosProject\leaf_tagging\data\ver5'

columns = ['image', 'y'] + [f'x_{i}' for i in range(14)]
using_train_test_files = True
if using_train_test_files:
    # train_df = pd.read_csv(fr'{data_path}\LeavesDataTrain.csv', names=columns, header=None)
    train_df = pd.read_csv(fr'{data_path}\train.csv', index_col=0)
    # test_df = pd.read_csv(fr'{data_path}\LeavesDataTest.csv', names=columns, header=None)
    test_df = pd.read_csv(fr'{data_path}\test.csv', index_col=0)
    cols_without_image_and_label = list(train_df.columns)
    cols_without_image_and_label.remove('Image')
    cols_without_image_and_label.remove('image')
    cols_without_image_and_label.remove('image_original')
    cols_without_image_and_label.remove('Label')
    y_train = train_df.loc[:, 'Label']
    x_train = train_df.loc[:, cols_without_image_and_label]

    y_test = test_df.loc[:, 'Label']
    x_test = test_df.loc[:, cols_without_image_and_label]

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    # model = XGBClassifier()
    # model = RandomForestClassifier()
    model = SVC()
    # model = DecisionTreeClassifier()
    # model = LogisticRegression()
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
else:
    chosen_file = fr'{data_path}\ver2\Predictions350.csv'
    data = pd.read_csv(chosen_file, names=columns, header=None)
    y = data.iloc[:, 1]
    x = data.iloc[:, 2:]
    # scaler = StandardScaler()
    # x = scaler.fit_transform(x)
    model = LogisticRegression()
    scores = cross_val_score(model, x, y, cv=10)
    print(scores)
    print(np.mean(scores))



