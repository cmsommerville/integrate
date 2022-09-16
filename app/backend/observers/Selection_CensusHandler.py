import os
import requests
import pandas as pd
from typing import Union, List
from flask import request
from app.shared import BaseObserver, upload_file, NoFileProvidedException

from ..classes import CensusHandler
from ..models import Model_SelectionCensusDetail, Model_SelectionPlan
from ..observables import Observable_SelectionPlan
from ..schemas import Schema_SelectionCensusSet, Schema_SelectionCensusDetail

HOSTNAME = os.getenv('HOSTNAME')

class Observer_SelectionCensusHandler(BaseObserver): 

    def __init__(self):
        pass

    def subscribe(self): 
        Observable_SelectionPlan.subscribe(self)

    @classmethod
    def post(cls, plans: Union[Model_SelectionPlan, List[Model_SelectionPlan]]): 
        print("In Observer_SelectionCensusHandler...")

        _plans = []
        if type(plans) != list: 
            _plans = [plans]
        else: 
            _plans = [*plans]

        for plan in _plans:

            try: 
                df, filename = upload_file(request, '/files')
            except NoFileProvidedException:
                df = pd.DataFrame() 
                filename = None
            except Exception as e:
                return {'error': str(e)}, 400

            # init census instance and return a dictionary of the census set
            census = CensusHandler(plan.selection_plan_id, df)
            census.process()
            dict_census_set = census.to_census_set_dict(selection_census_filename=filename)
            census_details = dict_census_set.pop('census_details')

            # validate census set and load model instance
            _schema_instance = Schema_SelectionCensusSet()
            model_instance = _schema_instance.load(dict_census_set)

            # save set to database
            model_instance.save_to_db()
            set_id = model_instance.selection_census_set_id

            # save details to databasee
            _detail_schema_instance = Schema_SelectionCensusDetail(many=True)
            models = _detail_schema_instance.load([{
                **d, 
                'selection_census_set_id': set_id,
            } for d in census_details])
            Model_SelectionCensusDetail.save_all_to_db(models)

            # set census set id on plan record
            requests.patch(f'{HOSTNAME}/api/crud/selection/plan/{plan.selection_plan_id}', json={
                'selection_census_set_id': set_id
            })


observer_selection_census_handler = Observer_SelectionCensusHandler()
