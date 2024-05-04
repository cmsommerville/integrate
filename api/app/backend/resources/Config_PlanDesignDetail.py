from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import (
    Model_ConfigPlanDesignDetail_Benefit,
    Model_ConfigPlanDesignDetail_PlanDesign,
)
from ..schemas import (
    Schema_ConfigPlanDesignDetail_Benefit,
    Schema_ConfigPlanDesignDetail_PlanDesign,
)


class CRUD_ConfigPlanDesignDetail_Benefit(BaseCRUDResource):
    model = Model_ConfigPlanDesignDetail_Benefit
    schema = Schema_ConfigPlanDesignDetail_Benefit()


class CRUD_ConfigPlanDesignDetail_Benefit_List(BaseCRUDResourceList):
    model = Model_ConfigPlanDesignDetail_Benefit
    schema = Schema_ConfigPlanDesignDetail_Benefit(many=True)


class CRUD_ConfigPlanDesignDetail_PlanDesign(BaseCRUDResource):
    model = Model_ConfigPlanDesignDetail_PlanDesign
    schema = Schema_ConfigPlanDesignDetail_PlanDesign()


class CRUD_ConfigPlanDesignDetail_PlanDesign_List(BaseCRUDResourceList):
    model = Model_ConfigPlanDesignDetail_PlanDesign
    schema = Schema_ConfigPlanDesignDetail_PlanDesign(many=True)
