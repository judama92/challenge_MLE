import pickle
import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime

class DelayModel:

    def __init__(
        self
    ):
        self._model = self.load_model('./challenge/delay_model.pkl')
        self.top_10_features = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

    def get_min_diff(self, 
                     data: pd.DataFrame
    ):
        """
        Calculate difference in minutes between Data-O (Datetime of flight operation) 
        and Date-I (Scheduled datetime of the flight).

        Args:
            data (Dataframe): It is a Dataframe with both columns (Data-O and Data-I) 
                                    to calculate the difference.

        Returns:
            (Dataframe): The Dataframe with a new column that contains the difference in minutes
                        between columns Data-O and Date-I.
        """
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
        return min_diff
    
    def delay(self, 
              data: pd.DataFrame, 
              target_column:str
    ):
        """
        Calculate if the delay is over 15 minutes.

        Args:
            data (Dataframe): It is a Dataframe with min_diff column.

        Returns:
            (Dataframe): The Dataframe with a new column that represents 1 if min_diff > 15, 0 if not.
        """
        data['min_diff'] = data.apply(self.get_min_diff, axis=1)
        threshold_in_minutes = 15
        delay_target = np.where(data["min_diff"] > threshold_in_minutes, 1, 0)
        return pd.DataFrame({target_column: delay_target}, index=data.index)

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        #data = self.delay(data)
        if target_column:
            target = self.delay(data, target_column)
        
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)
        features = features.reindex(columns=self.top_10_features, fill_value=0)
        return (features, target) if target_column else features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)
        n_y0 = int((target == 0).sum())
        n_y1 = int((target == 1).sum())
        scale = n_y0 / n_y1
        model=XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model=model.fit(x_train, y_train)

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        return self._model.predict(features).tolist()
    
    def save_model(self, filepath: str) -> None:
        """
        Save the trained model to a file.

        Args:
            filepath (str): path to save the model.
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self._model, f)

    def load_model(self, filepath: str) -> None:
        """
        Load a trained model from a file.

        Args:
            filepath (str): path to load the model from.
        """
        with open(filepath, 'rb') as f:
            return pickle.load(f)

def main():
    data = pd.read_csv("./data/data.csv")
    model = DelayModel()
    features, target = model.preprocess(data, target_column="delay")
    model.fit(features, target)
    model.save_model("./challenge/delay_model.pkl")
    model.load_model("./challenge/delay_model.pkl")
    sample_features = features.iloc[:5]
    predictions = model.predict(sample_features)

    print("Predicciones en muestras de prueba:", predictions)

if __name__ == "__main__":
    main()
