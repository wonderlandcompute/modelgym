import lightgbm as lgb
import numpy as np

from modelgym.models import Model
import hyperopt as hp


class LGBMClassifier(Model):
    def __init__(self, params=None):
        """
        :param params (dict or None): parameters for model.
                             If None default params are fetched.
        :param learning_task (str): set type of task(classification, regression, ...)
        """
        self.params = {'objective': 'binary', 'metric': 'binary_logloss'}
        self.params.update(params)
        self.n_estimators = self.params.pop('n_estimators', 1)
        self.model = None

    def _convert_to_dataset(self, data, label, cat_cols=None):
        return lgb.Dataset(data, label)

    def fit(self, dataset, weights=None):
        """
        :param X (np.array, shape (n_samples, n_features)): the input data
        :param y (np.array, shape (n_samples, ) or (n_samples, n_outputs)): the target data
        :param weights (np.array, shape (n_samples, ) or (n_samples, n_outputs) or None): weights of the data
        :return: self
        """
        dtrain = self._convert_to_dataset(dataset.X, dataset.y)
        self.model = lgb.train(self.params, dtrain, num_boost_round=self.n_estimators, verbose_eval=False)
        return self

    def save_snapshot(self, filename):
        """
        :return: serializable internal model state snapshot.

        """
        assert self.model, "model is not fitted"
        return self.model.save_binary(filename)

    def load_from_snapshot(self, filename):
        """
        :snapshot serializable internal model state
        loads from serializable internal model state snapshot.
        """
        return lgb.Booster(model_file=filename)

    def predict(self, dataset):
        """
        :param X (np.array, shape (n_samples, n_features)): the input data
        :return: np.array, shape (n_samples, ) or (n_samples, n_outputs)
        """
        return np.argmax(self.model.predict(dataset.X), axis=1)

    def is_possible_predict_proba(self):
        """
        :return: bool, whether model can predict proba
        """
        return True

    def predict_proba(self, dataset):
        """
        :param X (np.array, shape (n_samples, n_features)): the input data
        :return: np.array, shape (n_samples, n_classes)
        """
        return self.model.predict(dataset.X)

    @staticmethod
    def get_default_parameter_space():
        """
        :return: dict of DistributionWrappers
        """
        return {
          'learning_rate':           hp.loguniform('learning_rate', -7, 0),
          'num_leaves':              hp.qloguniform('num_leaves', 0, 7, 1),
          'feature_fraction':        hp.uniform('feature_fraction', 0.5, 1),
          'bagging_fraction':        hp.uniform('bagging_fraction', 0.5, 1),
          'min_data_in_leaf':        hp.qloguniform('min_data_in_leaf', 0, 6, 1),
          'min_sum_hessian_in_leaf': hp.loguniform('min_sum_hessian_in_leaf', -16, 5),
          'lambda_l1':               hp.loguniform('lambda_l1', -16, 2),
          'lambda_l2':               hp.loguniform('lambda_l2', -16, 2),
        }


class LGBMRegressor(Model):
    def __init__(self, params=None):
        """
        :param params (dict or None): parameters for model.
                             If None default params are fetched.
        :param learning_task (str): set type of task(classification, regression, ...)
        """
        self.params = {'objective': 'mean_squared_error', 'metric': 'l2'}
        self.params.update(params)
        self.n_estimators = self.params.pop('n_estimators', 1)
        self.model = None

    def _convert_to_dataset(self, data, label, cat_cols=None):
        return lgb.Dataset(data, label)

    def fit(self, dataset, weights=None):
        """
        :param X (np.array, shape (n_samples, n_features)): the input data
        :param y (np.array, shape (n_samples, ) or (n_samples, n_outputs)): the target data
        :param weights (np.array, shape (n_samples, ) or (n_samples, n_outputs) or None): weights of the data
        :return: self
        """
        dtrain = self._convert_to_dataset(dataset.X, dataset.y)
        self.model = lgb.train(self.params, dtrain, num_boost_round=self.n_estimators, verbose_eval=False)
        return self

    def save_snapshot(self, filename):
        """
        :return: serializable internal model state snapshot.

        """
        assert self.model, "model is not fitted"
        return self.model.save_binary(filename)

    def load_from_snapshot(self, filename):
        """
        :snapshot serializable internal model state
        loads from serializable internal model state snapshot.
        """
        return lgb.Booster(model_file=filename)

    def predict(self, dataset):
        """
        :param X (np.array, shape (n_samples, n_features)): the input data
        :return: np.array, shape (n_samples, ) or (n_samples, n_outputs)
        """
        return self.model.predict(dataset.X)

    def is_possible_predict_proba(self):
        """
        :return: bool, whether model can predict proba
        """
        return False

    def predict_proba(self, dataset):
        """
        :param X (np.array, shape (n_samples, n_features)): the input data
        :return: np.array, shape (n_samples, n_classes)
        """
        raise ValueError("Regressor can't predict proba")

    @staticmethod
    def get_default_parameter_space():
        """
        :return: dict of DistributionWrappers
        """

        return {
            'learning_rate': hp.loguniform('learning_rate', -7, 0),
            'num_leaves': hp.qloguniform('num_leaves', 0, 7, 1),
            'feature_fraction': hp.uniform('feature_fraction', 0.5, 1),
            'bagging_fraction': hp.uniform('bagging_fraction', 0.5, 1),
            'min_data_in_leaf': hp.qloguniform('min_data_in_leaf', 0, 6, 1),
            'min_sum_hessian_in_leaf': hp.loguniform('min_sum_hessian_in_leaf', -16, 5),
            'lambda_l1': hp.loguniform('lambda_l1', -16, 2),
            'lambda_l2': hp.loguniform('lambda_l2', -16, 2),
        }

