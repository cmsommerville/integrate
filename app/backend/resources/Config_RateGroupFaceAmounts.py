import pandas as pd
from flask import request
from flask_restx import Resource
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import Model_ConfigRateGroupFaceAmounts, Model_ConfigProduct, Model_ConfigAttributeDetail
from ..schemas import Schema_ConfigRateGroupFaceAmounts

def face_amount_handler(data: dict, *args, **kwargs) -> dict:

    face_amounts = data.get('face_amounts')
    if face_amounts is None: 
        return {"status": "error", "msg": "Please send `face_amounts` property in the payload"}

    df_face_amounts = pd.DataFrame(face_amounts)

    vary_by_gender = data.get('vary_by_gender', False)
    vary_by_smoker_status = data.get('vary_by_smoker_status', False)
    vary_by_relationship = data.get('vary_by_relationship', False)

    if vary_by_gender == False: 
        df_face_amounts['config_gender_detail_id'] = -1
    if vary_by_relationship == False:
        df_face_amounts['config_relationship_detail_id'] = -1
    if vary_by_smoker_status == False: 
        df_face_amounts['config_smoker_status_detail_id'] = -1

    df_face_amounts = df_face_amounts.drop_duplicates(subset=[
        'config_rate_group_id', 'config_gender_detail_id', 
        'config_smoker_status_detail_id', 'config_relationship_detail_id',
        'face_amount_value'])
    
    return df_face_amounts[[
        'config_rate_group_id', 'config_gender_detail_id', 
        'config_smoker_status_detail_id', 'config_relationship_detail_id',
        'face_amount_value'
    ]].to_dict('records')
        


class CRUD_ConfigRateGroupFaceAmounts_List(BaseCRUDResourceList): 
    model = Model_ConfigRateGroupFaceAmounts
    schema = Schema_ConfigRateGroupFaceAmounts(many=True)

    @classmethod
    def post(cls, *args, **kwargs):
        try: 
            data = request.get_json()
            dict_face_amounts = face_amount_handler(data)
            schema = Schema_ConfigRateGroupFaceAmounts(many=True)
            face_amounts = schema.load(dict_face_amounts)
            Model_ConfigRateGroupFaceAmounts.save_all_to_db(face_amounts)
            return schema.dump(face_amounts), 201
        except Exception as e: 
            return {"status": "error", "msg": str(e)}, 400
