from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import (
    Model_ConfigPlanDesignSet_Coverage,
    Model_ConfigPlanDesignSet_Product,
)
from ..schemas import (
    Schema_ConfigPlanDesignSet_Coverage,
    Schema_ConfigPlanDesignSet_Product,
)


class CRUD_ConfigPlanDesignSet_Coverage(BaseCRUDResource):
    model = Model_ConfigPlanDesignSet_Coverage
    schema = Schema_ConfigPlanDesignSet_Coverage()


class CRUD_ConfigPlanDesignSet_Coverage_List(BaseCRUDResourceList):
    model = Model_ConfigPlanDesignSet_Coverage
    schema = Schema_ConfigPlanDesignSet_Coverage(many=True)


class CRUD_ConfigPlanDesignSet_Product(BaseCRUDResource):
    model = Model_ConfigPlanDesignSet_Product
    schema = Schema_ConfigPlanDesignSet_Product()


class CRUD_ConfigPlanDesignSet_Product_List(BaseCRUDResourceList):
    model = Model_ConfigPlanDesignSet_Product
    schema = Schema_ConfigPlanDesignSet_Product(many=True)
