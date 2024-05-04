from __future__ import annotations
import numpy as np
import pandas as pd
from typing import List
from decimal import Decimal


class CustomGenderDistribution: 
    """
    Custom class used to type the Census Builder for gender distribution data
    """
    def __init__(self, data: dict, *args, **kwargs):
        self.config_gender_detail_id = data.get('config_attr_detail_id')
        self.gender_weight = data.get('weight')

    def to_dict(self):
        return {
            'config_gender_detail_id': self.config_gender_detail_id, 
            'gender_weight': self.gender_weight, 
        }

    @classmethod
    def from_list(cls, data: List[dict]) -> List[dict]: 
        if data is None:
            raise Exception('Please provide gender distribution data')
        return [cls(item) for item in data]


class CustomSmokerStatusDistribution: 
    """
    Custom class used to type the Census Builder for smoker status distribution data
    """
    def __init__(self, data: dict, *args, **kwargs):
        self.config_smoker_status_detail_id = data.get('config_attr_detail_id')
        self.smoker_status_weight = data.get('weight')

    def to_dict(self):
        return {
            'config_smoker_status_detail_id': self.config_smoker_status_detail_id, 
            'smoker_status_weight': self.smoker_status_weight, 
        }

    @classmethod
    def from_list(cls, data: List[dict]) -> List[dict]: 
        if data is None:
            raise Exception('Please provide smoker status distribution data')
        return [cls(item) for item in data]


class CustomAgeDistribution: 
    """
    Custom class used to type the Census Builder for age distribution data
    """
    def __init__(self, data: dict, *args, **kwargs):
        self.age_value = data.get('age_value')
        self.age_weight = data.get('weight')

    def to_dict(self):
        return {
            'age_value': self.age_value, 
            'age_weight': self.age_weight, 
        }

    @classmethod
    def from_list(cls, data: List[dict]) -> List[dict]: 
        if data is None:
            raise Exception('Please provide age distribution data')
        return [cls(item) for item in data]


class CensusBuilder: 

    def __init__(
        self, 
        gender_distribution: List[CustomGenderDistribution], 
        smoker_status_distribution: List[CustomSmokerStatusDistribution], 
        age_distribution: List[CustomAgeDistribution], 
        *args, **kwargs): 

        self.gender_distribution = [item.to_dict() for item in gender_distribution]
        self.smoker_status_distribution = [item.to_dict() for item in smoker_status_distribution]
        self.age_distribution = [item.to_dict() for item in age_distribution]

        self.df_gender_dist = self._to_df(self.gender_distribution)
        self.df_smoker_dist = self._to_df(self.smoker_status_distribution)
        self.df_age_dist = self._to_df(self.age_distribution)

    def _to_df(self, dist): 
        df = pd.DataFrame(dist)
        df['__DUMMY__'] = 1
        return df

    def generate_census_detail(self):
        """
        Cross join the three distributional assumptions to generate a final census
        """
        # cross join age distribution to smoker status distribution
        df = self.df_age_dist.merge(self.df_smoker_dist, on='__DUMMY__', how='inner')
        # cross join result to gender distribution 
        df = df.merge(self.df_gender_dist, on='__DUMMY__', how='inner')
        # calculate weight as product of three weights
        df['selection_census_weight'] = df['gender_weight'] * df['smoker_status_weight'] * df['age_weight']
        # normalize weights
        normalizer = Decimal('10') ** (-int(np.log10(df['selection_census_weight'].mean())))
        df['selection_census_weight'] = df['selection_census_weight'] * normalizer
        # select output columns 
        df = df[['config_gender_detail_id', 'config_smoker_status_detail_id', 'age_value', 'selection_census_weight']]
        return df.to_dict('records')

