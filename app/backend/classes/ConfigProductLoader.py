from typing import Union
from marshmallow import ValidationError, EXCLUDE
from app.extensions import db
from ..models import (
    Model_RefCensusStrategy,
    Model_RefComparisonOperator,
    Model_RefDataTypes,
    Model_RefRatingStrategy,
    Model_RefRateFrequency,
    Model_RefStates,
    Model_RefUnitCode,
    Model_ConfigAgeDistributionSet,
    Model_ConfigAttributeDetail,
    Model_ConfigBenefit,
    Model_ConfigProductVariation,
    Model_ConfigRateGroup,
    Model_ConfigRateTableSet,
    Model_ConfigRatingMapperCollection,
)
from ..schemas import (
    ProductLoaderSchema,
    Schema_ConfigBenefit_CRUD,
    Schema_ConfigBenefitVariation,
    Schema_ConfigFactorSet,
    Schema_ConfigProduct,
    Schema_ConfigProductState,
    Schema_ConfigProductVariation,
    Schema_ConfigProductVariationState,
    Schema_ConfigProvision,
    Schema_ConfigProvisionState,
    Schema_ConfigRateGroup,
    Schema_ConfigRateTableSet,
)


class AttrGetterMixin:
    @classmethod
    def get_rating_strategy_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_RefRatingStrategy.find_one_by_attr({"ref_attr_code": code})
        return obj.ref_id if obj else None

    @classmethod
    def get_age_distribution_set_id(cls, label: Union[str, None]):
        if label is None:
            return None
        obj = Model_ConfigAgeDistributionSet.find_one_by_attr(
            {"config_age_distribution_set_label": label}
        )
        return obj.config_age_distribution_set_id if obj else None

    @classmethod
    def get_rating_mapper_collection_id(cls, label: Union[str, None]):
        if label is None:
            return None
        obj = Model_ConfigRatingMapperCollection.find_one_by_attr(
            {"config_rating_mapper_collection_label": label}
        )
        return obj.config_rating_mapper_collection_id if obj else None

    @classmethod
    def get_census_strategy_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_RefCensusStrategy.find_one_by_attr({"ref_attr_code": code})
        return obj.ref_id if obj else None

    @classmethod
    def get_data_type_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_RefDataTypes.find_one_by_attr({"ref_attr_code": code})
        return obj.ref_id if obj else None

    @classmethod
    def get_operator_id(cls, symbol: Union[str, None]):
        if symbol is None:
            raise ValueError("Symbol must not be null")
        obj = Model_RefComparisonOperator.find_one_by_attr({"ref_attr_symbol": symbol})
        if obj:
            return obj.ref_id
        raise ValueError("Symbol must not be null")

    @classmethod
    def get_rating_attr_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_ConfigAttributeDetail.find_one_by_attr(
            {"config_attr_detail_code": code}
        )
        if obj:
            return obj.config_attr_detail_id
        return None

    @classmethod
    def get_rating_mapper_collection(cls, label: Union[str, None]):
        if label is None:
            return None
        obj = Model_ConfigRatingMapperCollection.find_one_by_attr(
            {"config_rating_mapper_collection_label": label}
        )
        return obj.config_rating_mapper_collection_id if obj else None

    @classmethod
    def get_config_attr_detail_id(cls, code: Union[str, None], config_attr_set_id: int):
        if code is None:
            return None
        obj = Model_ConfigAttributeDetail.find_one_by_attr(
            {"config_attr_detail_code": code, "config_attr_set_id": config_attr_set_id}
        )
        return obj.config_attr_detail_id if obj else None

    @classmethod
    def get_rate_group_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_ConfigRateGroup.find_one_by_attr({"config_rate_group_code": code})
        return obj.config_rate_group_id if obj else None

    @classmethod
    def get_unit_type_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_RefUnitCode.find_one_by_attr({"ref_attr_code": code})
        return obj.ref_id if obj else None

    @classmethod
    def get_rate_table_set_id(cls, label: Union[str, None], benefit_id: int):
        if label is None:
            return None
        obj = Model_ConfigRateTableSet.find_one_by_attr(
            {"config_rate_table_set_label": label, "config_benefit_id": benefit_id}
        )
        if not obj:
            raise ValidationError("Invalid rate table")
        return obj.config_rate_table_set_id

    @classmethod
    def get_benefit_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_ConfigBenefit.find_one_by_attr({"config_benefit_code": code})
        if not obj:
            raise ValidationError("Invalid benefit")
        return obj.config_benefit_id

    @classmethod
    def get_product_variation_id(cls, code: Union[str, None]):
        if code is None:
            return None
        obj = Model_ConfigProductVariation.find_one_by_attr(
            {"config_product_variation_code": code}
        )
        if not obj:
            raise ValidationError("Invalid product variation")
        return obj.config_product_variation_id

    @classmethod
    def get_rate_frequency_id(cls, code: str):
        if code is None:
            raise ValidationError("rate_frequency_code must be non-null")
        obj = Model_RefRateFrequency.find_one_by_attr({"ref_attr_code": code})
        if not obj:
            raise ValidationError("Invalid rate frequency")
        return obj.ref_id


class ConfigBenefitLoader(AttrGetterMixin):
    def __init__(
        self, benefits_data, benefit_variations_data, rate_tables_data, **kwargs
    ):
        self.benefits_data = benefits_data
        self.benefit_variations_data = benefit_variations_data
        self.rate_tables_data = rate_tables_data

    @classmethod
    def process_rate_table_detail(cls, rate, rate_table_set):
        rate_frequency_code = rate.pop("rate_frequency_code")
        rate["rate_frequency_id"] = cls.get_rate_frequency_id(rate_frequency_code)

        for i in range(1, 7):
            rating_attr_code = rate.pop(f"rating_attr_code{i}", None)
            if rating_attr_code is None:
                continue
            collection_id = rate_table_set.get(f"rating_mapper_collection_id{i}")
            if collection_id is None:
                continue
            collection = Model_ConfigRatingMapperCollection.find_one(collection_id)
            rate[f"rating_attr_id{i}"] = cls.get_config_attr_detail_id(
                rating_attr_code, collection.config_attribute_set_id
            )
        return rate

    @classmethod
    def process_rate_table_set(cls, rate_table):
        rt = {**rate_table}
        config_benefit_code = rt.pop("config_benefit_code")
        rt["config_benefit_id"] = cls.get_benefit_id(config_benefit_code)
        for i in range(1, 7):
            collection_label = rt.pop(f"rating_mapper_collection_label{i}", None)
            if collection_label is None:
                continue
            rt[f"rating_mapper_collection_id{i}"] = cls.get_rating_mapper_collection_id(
                collection_label
            )

        rt["rates"] = [cls.process_rate_table_detail(rate, rt) for rate in rt["rates"]]

        return rt

    @classmethod
    def process_benefit(cls, bnft):
        benefit = {**bnft}
        unit_type_code = benefit.pop("unit_type_code")
        benefit["unit_type_id"] = cls.get_unit_type_id(unit_type_code)

        config_rate_group_code = benefit.pop("config_rate_group_code")
        benefit["config_rate_group_id"] = cls.get_rate_group_id(config_rate_group_code)
        return benefit

    @classmethod
    def process_benefit_variation_state(cls, bvs_list, ref_states, benefit_id):
        state_mapper = {obj.state_code: obj for obj in ref_states}
        EXCLUDE_FIELDS = [
            "config_benefit_variation_state_code",
            "config_rate_table_set_label",
        ]
        return [
            {
                **{k: v for k, v in bvs.items() if k not in EXCLUDE_FIELDS},
                "state_id": state_mapper[
                    bvs["config_benefit_variation_state_code"]
                ].state_id,
                "config_rate_table_set_id": cls.get_rate_table_set_id(
                    bvs["config_rate_table_set_label"], benefit_id
                ),
            }
            for bvs in bvs_list
        ]

    @classmethod
    def process_benefit_variation(cls, bv, ref_states):
        return {
            "config_benefit_id": cls.get_benefit_id(bv["config_benefit_code"]),
            "config_product_variation_id": cls.get_product_variation_id(
                bv["config_product_variation_code"]
            ),
            "states": cls.process_benefit_variation_state(
                bv["states"], ref_states, cls.get_benefit_id(bv["config_benefit_code"])
            ),
        }

    def benefit_loader(self, config_product_id: int):
        schema = Schema_ConfigBenefit_CRUD(many=True, unknown=EXCLUDE)
        data = [
            {
                **self.process_benefit(bnft),
                "config_product_id": config_product_id,
                "benefit_variation_states": [],
                "duration_sets": [],
            }
            for bnft in self.benefits_data
        ]
        objs = schema.load(data)
        db.session.add_all(objs)
        db.session.flush()
        self.benefits = objs
        return schema.dump(self.benefits)

    def rate_table_loader(self):
        schema = Schema_ConfigRateTableSet(many=True, unknown=EXCLUDE)
        rate_tables = [self.process_rate_table_set(rt) for rt in self.rate_tables_data]
        objs = schema.load(rate_tables)
        db.session.add_all(objs)
        db.session.flush()
        self.rate_tables = objs
        return schema.dump(self.rate_tables)

    def benefit_variations_loader(self):
        schema = Schema_ConfigBenefitVariation(many=True, unknown=EXCLUDE)
        data = [
            {**self.process_benefit_variation(bv, self.ref_states)}
            for bv in self.benefit_variations_data
        ]
        objs = schema.load(data)
        db.session.add_all(objs)
        db.session.flush()
        self.benefit_variations = objs
        return schema.dump(self.benefit_variations)

    def save_to_db(self, product_id, commit=True, **kwargs):
        self.benefit_loader(product_id)
        self.rate_table_loader()
        self.benefit_variations_loader()
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()


class ConfigProvisionLoader(AttrGetterMixin):
    def __init__(self, provisions_data, **kwargs):
        self.provisions_data = provisions_data

    @classmethod
    def process_factor_rule(cls, rule):
        _rule = {
            **rule,
            "comparison_operator_id": cls.get_operator_id(
                rule["comparison_operator_symbol"]
            ),
            "comparison_attr_data_type_id": cls.get_data_type_id(
                rule["comparison_attr_data_type_code"]
            ),
        }
        _rule.pop("comparison_operator_symbol")
        _rule.pop("comparison_attr_data_type_code")
        return _rule

    @classmethod
    def process_factor_value(cls, value):
        val = {**value}
        for i in range(1, 7):
            if f"rating_attr_code{i}" not in val.keys():
                continue
            rating_attr_code = val.pop(f"rating_attr_code{i}")
            val[f"rating_attr_id{i}"] = cls.get_rating_attr_id(rating_attr_code)
        return val

    def provision_loader(self, config_product_id: int):
        schema = Schema_ConfigProvision(
            many=True,
            unknown=EXCLUDE,
        )
        data = [
            {
                "config_product_id": config_product_id,
                "config_provision_data_type_id": self.get_data_type_id(
                    p["config_provision_data_type_code"]
                ),
                **{
                    k: v
                    for k, v in p.items()
                    if k not in ["factors", "benefit_provisions", "states"]
                },
            }
            for p in self.provisions_data
        ]
        objs = schema.load(data)
        db.session.add_all(objs)
        db.session.flush()
        self.provisions = objs

    def provision_state_loader(self):
        schema = Schema_ConfigProvisionState(many=True, unknown=EXCLUDE)
        prov_mapper = {prov.config_provision_code: prov for prov in self.provisions}
        state_mapper = {s.state_code: s for s in self.ref_states}

        provision_states = []
        for pv in self.provisions_data:
            pv_obj = prov_mapper[pv["config_provision_code"]]
            states = pv["states"]

            data = [
                {
                    "config_provision_id": pv_obj.config_provision_id,
                    "state_id": state_mapper[
                        pvs["config_provision_state_code"]
                    ].state_id,
                    **pvs,
                }
                for pvs in states
            ]
            objs = schema.load(data)
            db.session.add_all(objs)
            db.session.flush()
            provision_states.extend(objs)
        self.provision_states = provision_states

    def factor_loader(self):
        schema = Schema_ConfigFactorSet(many=True, unknown=EXCLUDE)
        prov_mapper = {prov.config_provision_code: prov for prov in self.provisions}

        factor_sets = []
        for pv in self.provisions_data:
            pv_obj = prov_mapper[pv["config_provision_code"]]
            data = [
                {
                    **factor,
                    "config_provision_id": pv_obj.config_provision_id,
                    "factor_rules": [
                        self.process_factor_rule(rule)
                        for rule in factor["factor_rules"]
                    ],
                    "factor_values": [
                        self.process_factor_value(val)
                        for val in factor["factor_values"]
                    ],
                }
                for factor in pv["factors"]
            ]
            objs = schema.load(data)
            db.session.add_all(objs)
            db.session.flush()
            factor_sets.extend(objs)
        self.factors = factor_sets

    def save_to_db(self, product_id, commit=True, **kwargs):
        self.provision_loader(product_id)
        self.provision_state_loader()
        self.factor_loader()
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()


class ConfigProductLoader(AttrGetterMixin):
    schema = ProductLoaderSchema()

    def __init__(self, config):
        errs = self.schema.validate(config)
        if len(errs.keys()) > 0:
            raise ValidationError(str(errs))

        _config = self.schema.dump(config)
        self.product_states_data = _config.pop("states", [])
        self.product_variations_data = _config.pop("product_variations", [])
        self.rate_groups_data = _config.pop("rate_groups", [])
        self.benefits_data = _config.pop("benefits", [])
        self.provisions_data = _config.pop("provisions", [])
        self.rate_tables_data = _config.pop("rate_tables", [])
        self.benefit_variations_data = _config.pop("benefit_variations", [])
        self.product_data = _config

        self.ref_states = Model_RefStates.find_all()

    def product_loader(self):
        """
        Replace all the codes with IDs and create the product object
        """
        product_data = {**self.product_data}

        age_rating_strategy_code = product_data.pop("age_rating_strategy_code")
        age_rating_strategy_id = self.get_rating_strategy_id(age_rating_strategy_code)

        age_distribution_set_label = product_data.pop("age_distribution_set_label")
        age_distribution_set_id = self.get_age_distribution_set_id(
            age_distribution_set_label
        )

        employer_paid_census_strategy_code = product_data.pop(
            "employer_paid_census_strategy_code"
        )
        employer_paid_census_strategy_id = self.get_census_strategy_id(
            employer_paid_census_strategy_code
        )

        voluntary_census_strategy_code = product_data.pop(
            "voluntary_census_strategy_code"
        )
        voluntary_census_strategy_id = self.get_census_strategy_id(
            voluntary_census_strategy_code
        )

        rating_mapper_ids = []
        for i in range(1, 7):
            r = product_data.pop(f"rating_mapper_collection_label{i}")
            rating_mapper_ids.append(self.get_rating_mapper_collection_id(r))

        schema = Schema_ConfigProduct()
        product_data = {
            **product_data,
            "age_rating_strategy_id": age_rating_strategy_id,
            "age_distribution_set_id": age_distribution_set_id,
            "employer_paid_census_strategy_id": employer_paid_census_strategy_id,
            "voluntary_census_strategy_id": voluntary_census_strategy_id,
            **{
                f"rating_mapper_collection_id{i + 1}": _id
                for i, _id in enumerate(rating_mapper_ids)
            },
        }
        product_obj = schema.load(product_data)
        db.session.add(product_obj)
        db.session.flush()
        self.product = product_obj
        return schema.dump(self.product)

    def product_state_loader(self, config_product_id: int):
        """
        Replace all the codes with IDs and create the product object
        """
        schema = Schema_ConfigProductState(many=True)
        state_mapper = {obj.state_code: obj for obj in self.ref_states}

        product_states_data = [
            {
                "config_product_id": config_product_id,
                "state_id": state_mapper[ps["config_product_state_code"]].state_id,
                "config_product_state_effective_date": ps[
                    "config_product_state_effective_date"
                ],
                "config_product_state_expiration_date": ps[
                    "config_product_state_expiration_date"
                ],
            }
            for ps in self.product_states_data
        ]
        product_state_objs = schema.load(product_states_data)
        db.session.add_all(product_state_objs)
        db.session.flush()
        self.product_states = product_state_objs
        return schema.dump(self.product_states)

    def rate_group_loader(self, config_product_id: int):
        schema = Schema_ConfigRateGroup(many=True)
        rate_group_data = [
            {
                **rg,
                "config_product_id": config_product_id,
            }
            for rg in self.rate_groups_data
        ]
        objs = schema.load(rate_group_data)
        db.session.add_all(objs)
        db.session.flush()
        self.rate_groups = objs
        return schema.dump(self.rate_groups)

    def product_variation_loader(self, config_product_id: int):
        schema = Schema_ConfigProductVariation(many=True, unknown=EXCLUDE)
        data = [
            {**pv, "config_product_id": config_product_id}
            for pv in self.product_variations_data
        ]
        objs = schema.load(data)
        db.session.add_all(objs)
        db.session.flush()
        self.product_variations = objs
        return schema.dump(self.product_variations)

    def product_variation_state_loader(self):
        schema = Schema_ConfigProductVariationState(many=True, unknown=EXCLUDE)
        pv_mapper = {
            pv.config_product_variation_code: pv for pv in self.product_variations
        }
        state_mapper = {s.state_code: s for s in self.ref_states}

        product_variation_states = []
        for pv in self.product_variations_data:
            pv_obj = pv_mapper[pv["config_product_variation_code"]]
            states = pv["states"]

            data = [
                {
                    "config_product_variation_id": pv_obj.config_product_variation_id,
                    "state_id": state_mapper[
                        pvs["config_product_variation_state_code"]
                    ].state_id,
                    **pvs,
                }
                for pvs in states
            ]
            objs = schema.load(data)
            db.session.add_all(objs)
            db.session.flush()
            product_variation_states.extend(objs)
        self.product_variation_states = product_variation_states
        return schema.dump(self.product_variation_states)

    def save_to_db(self):
        try:
            product = self.product_loader()
            product_id = product["config_product_id"]
            self.product_state_loader(product_id)
            self.rate_group_loader(product_id)
            self.product_variation_loader(product_id)
            self.product_variation_state_loader()

            provision_loader = ConfigProvisionLoader(self.provisions_data)
            provision_loader.save_to_db(product_id, commit=False)

            benefit_loader = ConfigBenefitLoader(self.benefits_data)
            benefit_loader.save_to_db(product_id, commit=False)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
