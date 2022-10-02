from flask import request as flask_request
from typing import Union, List
from app.shared import BaseObserver

from ..models import Model_SelectionPlan, Model_SelectionRateGroupFaceAmounts
from ..observables import Observable_SelectionPlan

class Observer_SelectionPlan_DefaultFaceAmounts(BaseObserver):

    def __init__(self):
        pass

    def subscribe(self): 
        Observable_SelectionPlan.subscribe(self)

    def _change_handler(self, plans: Union[Model_SelectionPlan, List[Model_SelectionPlan]], *args, **kwargs):
        _FACE_AMOUNTS = []
        if type(plans) != list: 
            plans = [plans]

        for plan in plans: 
            rate_groups = plan.product.config_rate_groups

            for rate_group in rate_groups:  
                face_amounts = getattr(rate_group, 'face_amounts', None)
                if getattr(rate_group, 'face_amounts', None) is None:
                    continue
                _FACE_AMOUNTS.extend([
                    Model_SelectionRateGroupFaceAmounts(
                        selection_plan_id=plan.selection_plan_id, 
                        config_rate_group_face_amount_id=amt.config_rate_group_face_amount_id, 
                        config_rate_group_id=amt.config_rate_group_id, 
                        config_gender_detail_id=amt.config_gender_detail_id, 
                        config_smoker_status_detail_id=amt.config_smoker_status_detail_id, 
                        config_relationship_detail_id=amt.config_relationship_detail_id, 
                        face_amount_value=amt.face_amount_value
                    )
                    for amt in face_amounts
                ])

            Model_SelectionRateGroupFaceAmounts.delete_by_plan(plan.selection_plan_id)

        Model_SelectionRateGroupFaceAmounts.save_all_to_db(_FACE_AMOUNTS)

    def post(self, plans: Union[Model_SelectionPlan, List[Model_SelectionPlan]], request: flask_request, *args, **kwargs):
        print("In Observer_SelectionPlan_DefaultFaceAmounts...")
        self._change_handler(plans)


observer_selection_plan_default_face_amounts = Observer_SelectionPlan_DefaultFaceAmounts()
