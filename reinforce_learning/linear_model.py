import mglearn
import mglearn.datasets
from sklearn.datasets.samples_generator import make_blobs
from sklearn.datasets import load_breast_cancer
import pprint
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

class LinearModel():
    def linear_regression(self):
        mglearn.plots.plot_linear_regression_wave()
        X, y = mglearn.datasets.make_wave(n_samples=60)
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

        lr = LinearRegression().fit(X_train, y_train)

        print("lr.coef_: {}".format(lr.coef_))
        print("lr.intercept_: {}".format(lr.intercept_))
        print("trainset_score: {:.2f}".format(lr.score(X_train, y_train)))
        print("testset_score: {:.2f}".format(lr.score(X_test, y_test)))

        X, y = mglearn.datasets.load_extended_boston()
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
        lr = LinearRegression().fit(X_train, y_train)

        print("trainset_score: {:.2f}".format(lr.score(X_train, y_train)))
        print('testset_score: {:.2f}'.format(lr.score(X_test, y_test)))


        ridge = Ridge().fit(X_train, y_train)
        print('trainset score: {:.2f}'.format(ridge.score(X_train, y_train)))
        print('testset score: {:.2f}'.format(ridge.score(X_test, y_test)))

        # default alpha = 1 alpha값을 높이면 계수를 0에 가깝게 해준다.
        # 0에 가깝게 만들면 성능은 낮아지지만 일반화에는 도움이 됨
        # alpha=0.000001로 지정하면 LinearRegression에서 얻은 훈련세트 점수 0.95, 테스트세트 점수 0.61과 완벽하게 같음
        ridge10 = Ridge(alpha=10).fit(X_train, y_train)
        print('trainset score: {:.2f}'.format(ridge10.score(X_train, y_train)))
        print('testset score: {:.2f}'.format(ridge10.score(X_test, y_test)))

        ridge01 = Ridge(alpha=0.1).fit(X_train, y_train)
        print('trainset score: {:.2f}'.format(ridge10.score(X_train, y_train)))
        print('testset score: {:.2f}'.format(ridge10.score(X_test, y_test)))

        plt.plot(ridge10.coef_, '^', label='Ridge alpha=10')
        plt.plot(ridge.coef_, 's', label='Ridge alpha=1')
        plt.plot(ridge01.coef_, '^', label='Ridge alpha=0.1')

        plt.plot(lr.coef_, 'o', label='LinearRegression')
        plt.xlabel('feature_list')
        plt.ylabel('feature_size')
        plt.hlines(0, 0, len(lr.coef_))
        plt.ylim(-25, 25)
        plt.legend()
        plt.show()

        mglearn.plots.plot_ridge_n_samples()
        plt.show()

    def logisticregression(self):

        X, y = mglearn.datasets.make_forge()

        fig, axes = plt.subplots(1, 2, figsize=(10, 3))

        for model, ax in zip([LinearSVC(), LogisticRegression()], axes):
            clf = model.fit(X, y)
            mglearn.plots.plot_2d_separator(clf, X, fill=False, eps=0.5, ax=ax, alpha=0.7)
            mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
            ax.set_title("{}".format(clf.__class__.__name__))
            ax.set_xlabel("feature 0 ")
            ax.set_ylabel("feature 1")
        axes[0].legend()

        mglearn.plots.plot_linear_svc_regularization()
        plt.show()
# LinearModel().linear_regression()
LinearModel().logisticregression()
