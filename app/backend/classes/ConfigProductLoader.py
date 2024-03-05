from typing import Union, Dict
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
    Model_ConfigAgeBandSet,
    Model_ConfigAttributeDetail,
    Model_ConfigBenefit,
    Model_ConfigProductVariation,
    Model_ConfigProductVariationState,
    Model_ConfigProvision,
    Model_ConfigRateGroup,
    Model_ConfigRateTableSet,
    Model_ConfigRatingMapperCollection,
)
from ..schemas import (
    ProductLoaderSchema,
    Schema_ConfigBenefit_CRUD,
    Schema_ConfigBenefitDurationSet,
    Schema_ConfigBenefitProvision,
    Schema_ConfigBenefitVariationState,
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
    def get_age_band_set_id(cls, label: Union[str, None]):
        if label is None:
            return None
        obj = Model_ConfigAgeBandSet.find_one_by_attr(
            {"config_age_band_set_label": label}
        )
        return obj.config_age_band_set_id if obj else None

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
        self,
        config_product_id,
        benefits_data,
        benefit_variations_data,
        rate_tables_data,
        **kwargs,
    ):
        self.config_product_id = config_product_id
        self.benefits_data = benefits_data
        self.benefit_variations_data = benefit_variations_data
        self.rate_tables_data = rate_tables_data
        self.ref_states = Model_RefStates.find_all()

    @staticmethod
    def flatten(list_of_lists):
        return [x for xs in list_of_lists for x in xs]

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
    def process_benefit_variation(cls, bv, state_mapper, benefit_id, rate_table_mapper):
        return [
            {
                "config_benefit_id": benefit_id,
                "config_product_variation_state_id": state_mapper[
                    state["config_benefit_variation_state_code"]
                ].config_product_variation_state_id,
                "state_id": state_mapper[
                    state["config_benefit_variation_state_code"]
                ].state_id,
                "config_rate_table_set_id": rate_table_mapper[
                    state["config_rate_table_set_label"]
                ],
                **state,
            }
            for state in bv["states"]
        ]

    @classmethod
    def process_benefit_duration_set(cls, benefit_id, bnft_data):
        if bnft_data.get("duration_sets") is None:
            return []
        if not bnft_data["duration_sets"]:
            return []

        return [
            {**ds, "config_benefit_id": benefit_id} for ds in bnft_data["duration_sets"]
        ]

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

    def benefit_durations_loader(self):
        schema = Schema_ConfigBenefitDurationSet(many=True, unknown=EXCLUDE)
        bnft_mapper = {
            b.config_benefit_code: b
            for b in Model_ConfigBenefit.find_by_product(self.config_product_id)
        }

        data = []
        for bnft in self.benefits_data:
            benefit_id = bnft_mapper[bnft["config_benefit_code"]].config_benefit_id
            data.extend(self.process_benefit_duration_set(benefit_id, bnft))

        objs = schema.load(data)
        db.session.add_all(objs)
        db.session.flush()
        self.benefit_durations = objs

    def rate_table_loader(self):
        schema = Schema_ConfigRateTableSet(many=True, unknown=EXCLUDE)
        rate_tables = [self.process_rate_table_set(rt) for rt in self.rate_tables_data]
        objs = schema.load(rate_tables)
        db.session.add_all(objs)
        db.session.flush()
        self.rate_tables = objs
        return schema.dump(self.rate_tables)

    def benefit_variations_loader(self):
        schema = Schema_ConfigBenefitVariationState(many=True, unknown=EXCLUDE)
        data = []
        for bv in self.benefit_variations_data:
            benefit_id = self.get_benefit_id(bv["config_benefit_code"])
            product_variation = Model_ConfigProductVariation.find_one_by_attr(
                {
                    "config_product_id": self.config_product_id,
                    "config_product_variation_code": bv[
                        "config_product_variation_code"
                    ],
                }
            )
            product_variation_states = (
                Model_ConfigProductVariationState.find_by_product_variation(
                    product_variation.config_product_variation_id
                )
            )
            pv_state_mapper = {
                pvs.state.state_code: pvs for pvs in product_variation_states
            }

            rate_table_mapper = {
                rt.config_rate_table_set_label: rt.config_rate_table_set_id
                for rt in Model_ConfigRateTableSet.find_all_by_attr(
                    {"config_benefit_id": benefit_id}
                )
            }

            data.extend(
                self.process_benefit_variation(
                    bv, pv_state_mapper, benefit_id, rate_table_mapper
                )
            )

        objs = schema.load(data)
        db.session.add_all(objs)
        db.session.flush()
        self.benefit_variations = objs
        return schema.dump(self.benefit_variations)

    def save_to_db(self, product_id, commit=True, **kwargs):
        self.benefit_loader(product_id)
        self.benefit_durations_loader()
        self.rate_table_loader()
        self.benefit_variations_loader()
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()


class ConfigProvisionLoader(AttrGetterMixin):
    def __init__(self, product_id, provisions_data, **kwargs):
        self.config_product_id = product_id
        self.provisions_data = provisions_data
        self.ref_states = Model_RefStates.find_all()

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

    @classmethod
    def process_benefit_provision(
        cls,
        provision_obj: Model_ConfigProvision,
        prov_data,
        bnft_mapper: Dict[str, Model_ConfigBenefit],
    ):
        exclude = prov_data["benefit_provisions"].get("exclude", None)
        include = prov_data["benefit_provisions"].get("include", None)

        if include is not None:
            return [
                {
                    "config_benefit_id": bnft.config_benefit_id,
                    "config_provision_id": provision_obj.config_provision_id,
                }
                for code, bnft in bnft_mapper.items()
                if code in include
            ]

        return [
            {
                "config_benefit_id": bnft.config_benefit_id,
                "config_provision_id": provision_obj.config_provision_id,
            }
            for code, bnft in bnft_mapper.items()
            if code not in exclude
        ]

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

    def benefit_provisions_loader(self):
        schema = Schema_ConfigBenefitProvision(many=True, unknown=EXCLUDE)
        provisions_mapper = {
            p.config_provision_code: p
            for p in Model_ConfigProvision.find_all_by_attr(
                {"config_product_id": self.config_product_id}
            )
        }
        benefits_mapper = {
            b.config_benefit_code: b
            for b in Model_ConfigBenefit.find_all_by_attr(
                {"config_product_id": self.config_product_id}
            )
        }

        data = []
        for prov in self.provisions_data:
            provision = provisions_mapper[prov["config_provision_code"]]
            data.extend(
                self.process_benefit_provision(provision, prov, benefits_mapper)
            )

        objs = schema.load(data)
        db.session.add_all(objs)
        db.session.flush()
        self.benefit_provisions = objs

    def save_to_db(self, product_id, commit=True, **kwargs):
        self.provision_loader(product_id)
        self.provision_state_loader()
        self.factor_loader()
        self.benefit_provisions_loader()
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
                    "default_config_age_band_set_id": self.get_age_band_set_id(
                        pvs["default_config_age_band_set_label"]
                    ),
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

            benefit_loader = ConfigBenefitLoader(
                product_id,
                self.benefits_data,
                self.benefit_variations_data,
                self.rate_tables_data,
            )
            benefit_loader.save_to_db(product_id, commit=False)

            provision_loader = ConfigProvisionLoader(product_id, self.provisions_data)
            provision_loader.save_to_db(product_id, commit=False)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
