from decimal import Decimal
import numpy as np
import pandas as pd
from flask import request
from flask_restx import Resource
from ..models import Model_SelectionRateTable, Model_ConfigRateGroup, Model_SelectionRateGroupFaceAmounts
from ..schemas import Schema_ConfigRelationshipMapperSet

def roundByRateGroup(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Round the premium by rate group
    """
    df['modal_premium'] = df['modal_premium'].apply(lambda x: x.quantize(Decimal('0.01')))
    df = df.groupby(['selection_plan_id', 'selection_age_band_id', 
        'config_gender_detail_id', 'config_smoker_status_detail_id', 
        'config_relationship_detail_id', 'face_amount_value'], as_index=False).agg({"modal_premium": "sum"})
    
    return df

def roundTotalModalPremium(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Round the premium by rate group
    """
    df = df.groupby(['selection_plan_id', 'selection_age_band_id', 
        'config_gender_detail_id', 'config_smoker_status_detail_id', 
        'config_relationship_detail_id', 'face_amount_value'], as_index=False).agg({"modal_premium": "sum"})
    df['modal_premium'] = df['modal_premium'].apply(lambda x: x.quantize(Decimal('0.01')))
    
    return df
    

ROUNDING_STRATEGIES = {
    'rate_group': roundByRateGroup, 
    'total': roundTotalModalPremium
}

def premium_calculator(row, freq): 
    face_amount = row['face_amount_value'] if row['config_rate_group_id'] == row['_config_rate_group_id'] else Decimal('1')
    return face_amount / row['unit_value'] * row['annual_rate'] / Decimal(str(freq))

    # face_amount = Decimal(str(row['face_amount_value'])) if row['config_rate_group_id'] == row['_config_rate_group_id'] else Decimal('1')
    # return face_amount / Decimal(str(row['unit_value'])) * Decimal(str(row['annual_rate'])) / Decimal(str(freq))


class Resource_RatingPremiumCalculator(Resource): 
    
    @classmethod
    def post(cls, plan_id: int):
        data = request.get_json()
        if data is None:
            return {"status": "error", "message": "Please provide a body to thee POST request that contains `premium_frequency`"}

        # get modal premium frequency
        freq_obj = data.get('premium_frequency', {})
        freq = freq_obj.get('ref_attr_value', None)
        freq_id = freq_obj.get('ref_id', None)
        if freq is None:
            return {"status": "error", "message": "Please provide the `premium_frequency` as part of the POST request payload"}
        if freq <= 0:
            return {"status": "error", "message": "Please provide a positive `premium_frequency`"}

        # get rounding method function
        rounding_strategy = data.get('rounding_strategy', 'rate_group')
        rounding_method = ROUNDING_STRATEGIES.get(rounding_strategy)

        # get data for premium calculation
        rate_tables = Model_SelectionRateTable.find_by_plan(plan_id, as_pandas=True)
        rate_groups = Model_ConfigRateGroup.find_all_by_attr({
            'config_rate_group_id': rate_tables['config_rate_group_id'].unique().tolist()
        }, as_pandas=True)[['config_rate_group_id', 'unit_value']]
        face_amounts = Model_SelectionRateGroupFaceAmounts.find_by_plan(plan_id, as_pandas=True)
        face_amounts = face_amounts.rename(columns={col: '_' + col for col in face_amounts.columns})
        face_amounts_header = face_amounts.iloc[0].to_dict()

        # conditional join logic
        joins = ['selection_plan_id']
        if face_amounts_header.get('_config_gender_detail_id', -1) > 0: joins.append('config_gender_detail_id')
        if face_amounts_header.get('_config_smoker_status_detail_id', -1) > 0: joins.append('config_smoker_status_detail_id')
        if face_amounts_header.get('_config_relationship_detail_id', -1) > 0: joins.append('config_relationship_detail_id')

        rate_tables = rate_tables.merge(rate_groups, how='inner', on='config_rate_group_id')
        rate_tables = rate_tables.merge(face_amounts, how='inner', left_on=joins, right_on=['_' + col for col in joins])
        rate_tables = rate_tables.rename(columns={"_face_amount_value": "face_amount_value"})
        
        rate_tables['modal_premium'] = rate_tables.apply(lambda row: premium_calculator(row, freq), axis=1) 

        # apply rounding logic
        rate_tables = rounding_method(rate_tables)
        rate_tables['premium_frequency_id'] = freq_id
        rate_tables[['face_amount_value', 'modal_premium']] = rate_tables[['face_amount_value', 'modal_premium']].astype('float')
        return rate_tables.to_dict('records')
