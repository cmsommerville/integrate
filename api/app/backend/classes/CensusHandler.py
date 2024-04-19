from __future__ import annotations
import datetime
import numpy as np
import pandas as pd
from decimal import Decimal
from ..models import Model_SelectionPlan
from werkzeug.datastructures import FileStorage


def file_reader(file: FileStorage, *args, **kwargs):
    extension = file.filename.split('.')[-1]
    if extension in ['xlsx', 'xls']: 
        return pd.read_excel(file)
    if extension in ['csv', 'txt']: 
        return pd.read_csv(file)
    raise ValueError('Must provide a valid file')


class CensusHandler: 
    """
    Requires a user-provided census. This class augments any missing attributes with the product defaults.  
    """
    def __init__(self, plan_id: int, df_census: pd.DataFrame, *args, **kwargs):
        self.bias = kwargs.get('bias', 0.00001)
        self.df_census = df_census.copy()
        self.plan_id = plan_id
        self.plan = Model_SelectionPlan.find_one(plan_id)
        self.product = self.plan.product 
        self.gender_attr_set = self.product.gender_attr_set
        self.smoker_status_attr_set = self.product.smoker_status_attr_set
        self.gender_list = self.gender_attr_set.attributes
        self.smoker_status_list = self.smoker_status_attr_set.attributes
        self.composite_gender = next(g for g in self.gender_list if g.is_composite_id)
        self.composite_smoker_status = next(s for s in self.smoker_status_list if s.is_composite_id)

        self.df_gender = pd.DataFrame([
            {
                'gender_code': row.config_attr_detail_code, 
                'config_gender_detail_id': row.config_attr_detail_id, 
            }
            for row in self.gender_list
        ])

        self.df_smoker_status = pd.DataFrame([
            {
                'smoker_status_code': row.config_attr_detail_code, 
                'config_smoker_status_detail_id': row.config_attr_detail_id, 
            }
            for row in self.smoker_status_list
        ])

    def _get_default_smoker_status_distribution(self) -> pd.DataFrame:
        """
        Return the default smoker status distribution with a `_dummy` column
        """
        return pd.DataFrame([
            {
                '_dummy': 1, 
                'config_smoker_status_detail_id': dist.config_attr_detail_id, 
                '_weight_smoker_status': dist.weight, 
            }
            for dist in self.product.smoker_status_distribution_set.smoker_status_distribution
        ])

    def _get_default_gender_distribution(self) -> pd.DataFrame:
        """
        Return the default gender distribution with a `_dummy` column
        """
        return pd.DataFrame([
            {
                '_dummy': 1, 
                'config_gender_detail_id': dist.config_attr_detail_id, 
                '_weight_gender': dist.weight, 
            }
            for dist in self.product.gender_distribution_set.gender_distribution
        ])

    def _get_default_age_distribution(self) -> pd.DataFrame:
        """
        Return the default age distribution with a `_dummy` column
        """
        return pd.DataFrame([
            {
                '_dummy': 1, 
                'age_value': dist.age_value, 
                '_weight_age': dist.weight, 
            }
            for dist in self.product.age_distribution_set.age_distribution
        ])



    def _process_file(self):
        """
        Read the file into a Pandas dataframe. Conform values to database IDs. Filter and aggregate data as needed.
        """
        # calculate age value
        if 'age_value' in self.df_census.columns:
            pass
        elif 'date_of_birth' in self.df_census.columns:
            self.df_census['age_value'] = (int(self.plan.selection_plan_effective_date.strftime('%Y%m%d')) - 
                self.df_census['date_of_birth'].dt.strftime('%Y%m%d').astype(int)) // 10000
        else: 
            raise Exception("Please provide either an `age_value` column or `date_of_birth` column")

        # exclude prohibited issue ages
        min_issue_age = self.product.min_issue_age
        max_issue_age = self.product.max_issue_age
        self.df_census = self.df_census.query("age_value >= @min_issue_age & age_value <= @max_issue_age")

        # get gender attribute IDs
        self.df_census = self.df_census.merge(self.df_gender, how='left', on='gender_code')
        if self.df_census['config_gender_detail_id'].isna().sum() > 0:
            raise Exception("Gender codes provided in census which are not configured for this product")
        
        # get smoker status attributee IDs
        self.df_census = self.df_census.merge(self.df_smoker_status, how='left', on='smoker_status_code')
        if self.df_census['config_smoker_status_detail_id'].isna().sum() > 0:
            raise Exception("Smoker status codes provided in census which are not configured for this product")
        
        # add weight if not provided
        if 'selection_census_weight' not in self.df_census.columns:
            self.df_census['selection_census_weight'] = 1

        # aggregate census
        self.df_census = self.df_census.groupby(
            ['config_gender_detail_id', 'config_smoker_status_detail_id', 'age_value'], 
            as_index=False
        ).agg({'selection_census_weight': 'sum'})

        self.df_census['_dummy'] = 1

        return self.df_census
        
    def _generate_census(self, weight_column='selection_census_weight') -> pd.DataFrame: 
        """
        Helper method to generate the default census
        """
        # get default smoker status distribution
        df_ss_dist = self._get_default_smoker_status_distribution()

        # get default gender distribution
        df_g_dist = self._get_default_gender_distribution()

        # get default age distribution
        df_age_dist = self._get_default_age_distribution()

        df_census = df_ss_dist.merge(df_g_dist, how='inner', on='_dummy')
        df_census = df_census.merge(df_age_dist, how='inner', on='_dummy')
        df_census[weight_column] = df_census['_weight_age'] * df_census['_weight_smoker_status'] * df_census['_weight_gender']

        return df_census[['age_value', 'config_smoker_status_detail_id', 'config_gender_detail_id', weight_column]]


    def _handle_no_census(self) -> pd.DataFrame:
        """
        Handler for no census provided. Generate census from default distributions if composite assumptions are provided.
        """
        census_strategy = self.product.employer_paid_census_strategy if self.plan.is_employer_paid else self.product.voluntary_census_strategy

        if census_strategy.ref_attr_code.upper() == 'REQUIRED':
            raise Exception("A census is required for this product but was not provided. Please provide a census.")

        self.df_census = self._generate_census()
        return self.df_census


    def _handle_census_provided(self) -> pd.DataFrame: 
        """
        Handler for census provided. Use default gender/smoker status distributions if composite assumptions are provided in census.
        """

        self.df_census['_dummy'] = 1
        cols = self.df_census.columns
        # if census is missing smoker status, merge default SS distribution
        smoker_status_id_set = set(self.df_census['config_smoker_status_detail_id'].tolist())
        if len(smoker_status_id_set) > 1: 
            pass
        elif smoker_status_id_set[0] == self.composite_smoker_status.config_attr_detail_id:
            df_ss_dist = self._get_default_smoker_status_distribution()
            self.df_census = self.df_census.merge(df_ss_dist, how='inner', on='_dummy')
            self.df_census['selection_census_weight'] = self.df_census['selection_census_weight'] * self.df_census['_weight_smoker_status']
            self.df_census = self.df_census[cols]

        # if census is missing gender, merge default gender distribution
        gender_id_set = set(self.df_census['config_gender_detail_id'].tolist())
        if len(gender_id_set) > 1: 
            pass
        elif gender_id_set[0] == self.composite_gender.config_attr_detail_id:
            df_g_dist = self._get_default_gender_distribution()
            self.df_census = self.df_census.merge(df_g_dist, how='inner', on='_dummy')
            self.df_census['selection_census_weight'] = self.df_census['selection_census_weight'] * self.df_census['_weight_gender']
            self.df_census = self.df_census[cols]


        # get default census to add bias terms
        default_census = self._generate_census(weight_column='_bias')
        default_census = default_census.drop(columns=['_bias'])

        # full join the default and provided censuses
        self.df_census = default_census.merge(self.df_census, how='outer', 
            on=['config_gender_detail_id', 'config_smoker_status_detail_id', 'age_value'])
        self.df_census['selection_census_weight'] = self.df_census['selection_census_weight'].fillna(0)
        
        self.df_census = self.df_census.drop(columns=['_dummy'])
        return self.df_census


    def process(self):
        if len(self.df_census) == 0: 
            self._handle_no_census()
        else: 
            self._process_file()
            self._handle_census_provided()

        self.df_census['bias'] = self.bias

        normalizer = 10 ** (-int(np.log10(self.df_census['selection_census_weight'].mean())))
        self.df_census['selection_census_weight'] = pd.to_numeric(self.df_census['selection_census_weight']) * normalizer
        self.df_census['selection_census_weight'] = self.df_census[['bias', 'selection_census_weight']].max(axis=1)
        self.df_census = self.df_census.drop(columns=['bias'])

    def to_census_set_dict(self, *args, **kwargs): 
        default_census_description = f'Census created at {datetime.datetime.now()}'
        return {
            'selection_plan_id': self.plan_id,
            'selection_census_description': kwargs.get('selection_census_description', default_census_description), 
            'selection_census_filepath': kwargs.get('selection_census_filename'), 
            'census_details': self.df_census.to_dict('records')
        }