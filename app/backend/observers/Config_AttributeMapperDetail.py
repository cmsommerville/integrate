from typing import List
from app.shared import BaseObserver
from ..models import Model_ConfigAttributeMapperDetail, Model_ConfigAttributeSet, Model_RefAttrMapperType

def _generate_default_attribute_mappers(obj: Model_ConfigAttributeSet, mapper_types: dict,  *args, **kwargs) -> None:
    _mappers = []
    attrs = obj.attributes
    distincts = [attr for attr in attrs if not attr.is_composite_id]
    composite = next((attr for attr in attrs if attr.is_composite_id), None)
    if composite is None: 
        raise Exception("No composite attribute configured.")

    for dist in distincts: 
        # distinct to distinct
        _mappers.append(Model_ConfigAttributeMapperDetail(**{
            "config_attr_set_id": obj.config_attr_set_id,
            "config_attr_mapper_type_id": mapper_types['__dist_dist'], 
            "from_config_attr_detail_id": dist.config_attr_detail_id, 
            "to_config_attr_detail_id": dist.config_attr_detail_id, 
        }))
        # distinct to composite
        _mappers.append(Model_ConfigAttributeMapperDetail(**{
            "config_attr_set_id": obj.config_attr_set_id,
            "config_attr_mapper_type_id": mapper_types['__dist_comp'], 
            "from_config_attr_detail_id": dist.config_attr_detail_id, 
            "to_config_attr_detail_id": composite.config_attr_detail_id, 
        }))

    _mappers.append(Model_ConfigAttributeMapperDetail(**{
        "config_attr_set_id": obj.config_attr_set_id,
        "config_attr_mapper_type_id": mapper_types['__comp_comp'], 
        "from_config_attr_detail_id": composite.config_attr_detail_id, 
        "to_config_attr_detail_id": composite.config_attr_detail_id, 
    }))

    Model_ConfigAttributeSet.save_all_to_db(_mappers)
    return _mappers


def _handler(data, *args, **kwargs):
    _mapper_types = Model_RefAttrMapperType.find_all()
    mapper_types = {
        '__comp_comp': next((t for t in _mapper_types if t.ref_attr_code == '__comp_comp'), None), 
        '__dist_comp': next((t for t in _mapper_types if t.ref_attr_code == '__dist_comp'), None), 
        '__dist_dist': next((t for t in _mapper_types if t.ref_attr_code == '__dist_dist'), None), 
    }

    if type(data) == list:
        for item in data: 
            _generate_default_attribute_mappers(item, mapper_types)
    else:
        _generate_default_attribute_mappers(item, mapper_types)


Observer_ConfigAttributeMapperDetail_010 = BaseObserver(callback=_handler, methods=['POST'])