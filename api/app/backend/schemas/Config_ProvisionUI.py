from app.extensions import ma
from app.shared import BaseSchema

from ..models import Model_ConfigProvisionUI, Model_ConfigProvisionUI_Input, \
    Model_ConfigProvisionUI_Checkbox, Model_ConfigProvisionUI_Select, Model_ConfigProvisionUI_SelectItem


class Schema_ConfigProvisionUI_SelectItem(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUI_SelectItem
        load_instance = True
        include_relationships=True
        include_fk=True



class Schema_ConfigProvisionUI_Input(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUI_Input
        load_instance = True
        include_relationships=True
        include_fk=True

    component_type_code = ma.Constant('INPUT')


class Schema_ConfigProvisionUI_Checkbox(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUI_Checkbox
        load_instance = True
        include_relationships=True
        include_fk=True

    component_type_code = ma.Constant('CHECKBOX')


class Schema_ConfigProvisionUI_Select(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUI_Select
        load_instance = True
        include_relationships=True
        include_fk=True

    component_type_code = ma.Constant('SELECT')
    items = ma.List(ma.Nested(Schema_ConfigProvisionUI_SelectItem))


class Schema_ConfigProvisionUI(BaseSchema):
    class Meta:
        model = Model_ConfigProvisionUI
        load_instance = True
        include_relationships=True
        include_fk=True

    ui_input = ma.Nested(Schema_ConfigProvisionUI_Input)
    ui_checkbox = ma.Nested(Schema_ConfigProvisionUI_Checkbox)
    ui_select = ma.Nested(Schema_ConfigProvisionUI_Select)