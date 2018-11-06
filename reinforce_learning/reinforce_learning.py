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

class ReinforcementLearning():

    def forge(self):
        X, y = mglearn.datasets.make_forge()

        mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
        plt.legend(['class0', "class1"], loc=4)
        plt.xlabel("first_feature")
        plt.ylabel("second_feature")
        print("X.shape: {}".format(X.shape))
        plt.show()

    def make_wave(self):
        X, y = mglearn.datasets.make_wave(n_samples=80)
        plt.plot(X, y, 'o')
        plt.ylim(-3, 3)
        plt.xlabel("feature")
        plt.ylabel("target")
        plt.show()

    def breast_cancer(self):
        cancer=load_breast_cancer()
        pprint.pprint(cancer)
        print(type(cancer))
        print("cancer.keys() : \n{}".format(cancer.keys()))
        print("breast cancer data's shape:{}".format(cancer.data.shape))
        print("num_samples by class:\n{}".format({n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
        print("feature_name:\n{}".format(cancer.feature_names))

    def KNN_example(self):
        mglearn.plots.plot_knn_classification(n_neighbors=1)
        plt.show()
        mglearn.plots.plot_knn_classification(n_neighbors=3)
        plt.show()

    def KNN_train_test(self):
        X, y = mglearn.datasets.make_forge()
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
        clf = KNeighborsClassifier(n_neighbors=3)
        clf.fit(X_train, y_train)
        print("test set prediction: {}".format(clf.predict(X_test)))
        print("test set accuracy: {:.2f}".format(clf.score(X_test, y_test)))

    def KNeighborsclassifier(self):
        X, y = mglearn.datasets.make_forge()
        fig, axes = plt.subplots(1, 3, figsize=(10, 3))
        for n_neighbors, ax in zip([1, 3, 9], axes):
            # fit method는 self object를 return 함
            # 그래서 object create와 fit method를 한 줄에 쓸 수 있다.
            clf = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, y)
            mglearn.plots.plot_2d_separator(clf, X, fill=True, eps=0.5, ax=ax, alpha=0.4)
            mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
            ax.set_title("{} neighbor".format(n_neighbors))
            ax.set_xlabel("feature0")
            ax.set_ylabel("feature1")
        axes[0].legend(loc=3)
        plt.show()

    def breast_cancer_train_test(self):
        cancer = load_breast_cancer()
        X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target, random_state=66)
        training_accuracy = []
        test_accuracy = []
        # 1에서 10까지 n_neighbors를 적용
        neighbors_settings = range(1, 11)
        for n_neighbors in neighbors_settings:
            # create model
            clf = KNeighborsClassifier(n_neighbors=n_neighbors)
            clf.fit(X_train, y_train)
            # trainset accuracy save
            training_accuracy.append(clf.score(X_train, y_train))
            # testset accuracy save
            test_accuracy.append(clf.score(X_test, y_test))
        plt.plot(neighbors_settings, training_accuracy, label="training_accuracy")
        plt.plot(neighbors_settings, test_accuracy, label="test_accuracy")
        plt.ylabel("accuracy")
        plt.xlabel("n_neighbors")
        plt.legend()
        # plt.show()
        # k_neighbors_regression
        mglearn.plots.plot_knn_regression(n_neighbors=1)
        mglearn.plots.plot_knn_regression(n_neighbors=3)
        plt.show()

    def k_neighbors_regression(self):
        X, y = mglearn.datasets.make_wave(n_samples=40)

        # wave dataset을 train set과 test set으로 나눔
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

        # neighbors num을 3으로 해서 model의 object를 만듦
        reg = KNeighborsRegressor(n_neighbors=3)
        reg.fit(X_train, y_train)
        print('testset predict:\n{}'.format(reg.predict(X_test)))
        print('testset R^2: {:.2f}'.format(reg.score(X_test, y_test)))
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        # -3과 3 사이에 1000개의 data point를 만든다.
        line = np.linspace(-3, 3, 1000).reshape(-1, 1)
        for n_neighbors, ax in zip([1, 3, 9], axes):
            # 각 1, 3, 9개의 neighbors를 사용해 예측을 함
            reg = KNeighborsRegressor(n_neighbors=n_neighbors)
            reg.fit(X_train, y_train)
            ax.plot(line, reg.predict(line))
            ax.plot(X_train, y_train, '^', c=mglearn.cm2(0), markersize=8)
            ax.plot(X_test, y_test, 'v', c=mglearn.cm2(1), markersize=8)

            ax.set_title(
                "{} neighbor's train score: {:.2f} test score: {:.2f}".format(
                    n_neighbors, reg.score(X_train, y_train), reg.score(X_test, y_test)))
            ax.set_xlabel('feature')
            ax.set_ylabel('target')
        axes[0].legend(['model predict', 'train data/target', 'test data/target'], loc="best")
        plt.show()




# ReinforcementLearning().breast_cancer()
# ReinforcementLearning().KNN_example()
# ReinforcementLearning().KNN_train_test()
# ReinforcementLearning().KNeighborsclassifier()
# ReinforcementLearning().breast_cancer_train_test()
ReinforcementLearning().k_neighbors_regression()