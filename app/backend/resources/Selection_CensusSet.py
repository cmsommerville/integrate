import os
import datetime
import requests
import pandas as pd
from flask import request
from flask_restx import Resource
from werkzeug.datastructures import FileStorage
from app.extensions import api
from app.shared import BaseCRUDResource, BaseCRUDResourceList

from ..classes import CensusHandler, CensusBuilder, CustomAgeDistribution, CustomGenderDistribution, CustomSmokerStatusDistribution, file_reader
from ..models import Model_SelectionCensusSet, Model_SelectionCensusDetail
from ..schemas import Schema_SelectionCensusSet, Schema_SelectionCensusDetail

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
HOSTNAME = os.getenv('HOSTNAME')

class CRUD_SelectionCensusSet(BaseCRUDResource): 
    model = Model_SelectionCensusSet
    schema = Schema_SelectionCensusSet()

class CRUD_SelectionCensusSet_List(BaseCRUDResourceList): 
    model = Model_SelectionCensusSet
    schema = Schema_SelectionCensusSet(many=True)

class SelectionCensusSet_Dropdown(Resource):
    
    @classmethod
    def get(cls, plan_id: int):
        _schema = Schema_SelectionCensusSet(many=True, exclude=("census_details",))
        kwargs = request.args.to_dict()
        models = Model_SelectionCensusSet.find_all_by_attr({
            **kwargs,
            'selection_plan_id': plan_id,
        })
        return _schema.dump(models), 200


class SelectionCensusSet_UploadFile(Resource):

    @classmethod
    def post(cls, plan_id: int):
        args = upload_parser.parse_args()

        # read uploaded file
        try: 
            uploaded_file = args['file']
            df = file_reader(uploaded_file)
        except Exception as e:
            return {"status": "error", "message": "Could not read file"}

        # process the census
        try: 
            census = CensusHandler(plan_id, df)
            census.process()
            census_data = census.to_census_set_dict()
        except Exception as e: 
            return {"status": "error", "message": str(e)}
        
        _schema = Schema_SelectionCensusSet()
        _schema_detail_list = Schema_SelectionCensusDetail(many=True)
        _census_details = census_data.pop('census_details')

        # save census set 
        census_set = _schema.load(census_data)
        census_set.save_to_db()

        # add census details with census set id
        census_details = _schema_detail_list.load([
            {**detail, 'selection_census_set_id': census_set.selection_census_set_id}
            for detail in _census_details
        ])
        Model_SelectionCensusDetail.bulk_save_all_to_db(census_details)
        
        # set census set id on plan record
        requests.patch(f'{HOSTNAME}/api/crud/selection/plan/{plan_id}', json={
            'selection_census_set_id': census_set.selection_census_set_id
        })
        
        return _schema.dump(census_set), 201



class SelectionCensusSet_CensusBuilder(Resource):

    @classmethod
    def post(cls, plan_id: int):
        data = request.get_json()
        try: 
            gender_dist = CustomGenderDistribution.from_list(data.get('gender'))
            smoker_status_dist = CustomSmokerStatusDistribution.from_list(data.get('smoker_status'))
            age_dist = CustomAgeDistribution.from_list(data.get('age'))

            census_builder = CensusBuilder(gender_dist, smoker_status_dist, age_dist)
            _census_details = census_builder.generate_census_detail()
        except Exception as e:
            return {'status': "error", 'message': str(e)}, 400

        try: 
            _schema = Schema_SelectionCensusSet()
            _schema_detail_list = Schema_SelectionCensusDetail(many=True)
            census_set = _schema.load({
                'selection_plan_id': plan_id, 
                'selection_census_description': f'Census created at {datetime.datetime.now()}'
            })
            census_set.save_to_db()

            census_details = _schema_detail_list.load([
                {**detail, 'selection_census_set_id': census_set.selection_census_set_id}
                for detail in _census_details
            ])
            Model_SelectionCensusDetail.bulk_save_all_to_db(census_details)

        except Exception as e:
            return {'status': "error", 'message': str(e)}, 400

        # set census set id on plan record
        requests.patch(f'{HOSTNAME}/api/crud/selection/plan/{plan_id}', json={
            'selection_census_set_id': census_set.selection_census_set_id
        })
        return _schema.dump(census_set), 201