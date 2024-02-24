from flask import request
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.shared.errors import ExpiredRowVersionError
from app.shared import BaseCRUDResource, BaseCRUDResourceList
from ..models import (
    Model_ConfigProvision,
    Model_SelectionProvision,
    Model_ConfigFactor,
    Model_SelectionFactor,
)
from ..schemas import (
    Schema_SelectionProvision,
    Schema_SelectionProvision_UpdatePayloadValidator,
    Schema_SelectionProvision_CreatePayloadValidator,
)


class CRUD_SelectionProvision(BaseCRUDResource):
    model = Model_SelectionProvision
    schema = Schema_SelectionProvision()
    create_validator = Schema_SelectionProvision_CreatePayloadValidator()
    update_validator = Schema_SelectionProvision_UpdatePayloadValidator()

    @staticmethod
    def config_to_selection_factor(
        config_factor: Model_ConfigFactor, selection_provision_id: int
    ):
        return Model_SelectionFactor(
            selection_provision_id=selection_provision_id,
            config_factor_id=config_factor.config_factor_id,
            selection_rate_table_age_value=config_factor.rate_table_age_value,
            selection_rating_attr_id1=config_factor.rating_attr_id1,
            selection_rating_attr_id2=config_factor.rating_attr_id2,
            selection_rating_attr_id3=config_factor.rating_attr_id3,
            selection_rating_attr_id4=config_factor.rating_attr_id4,
            selection_rating_attr_id5=config_factor.rating_attr_id5,
            selection_rating_attr_id6=config_factor.rating_attr_id6,
            selection_factor_value=config_factor.factor_value,
        )

    @classmethod
    def _update_provision_no_commit(cls, id, data, *args, **kwargs):
        if data.get("version_id") is None:
            raise ValueError("Must pass version_id when updating an existing record")
        version_id = data.pop("version_id")
        validated_data = cls.update_validator.dump(data)
        rows_updated = cls.query.filter(
            cls.model.selection_provision_id == id, cls.version_id == version_id
        ).update(validated_data, synchronize_session="fetch")

        if rows_updated != 1:
            db.session.rollback()
            raise ExpiredRowVersionError(
                "This record has already been changed. Please refresh your data and try your request again"
            )

    @classmethod
    def get_first_valid_ruleset(
        cls,
        config_provision: Model_ConfigProvision,
        selection_provision: Model_SelectionProvision,
    ):
        # find first ruleset
        validated_factor_ruleset = next(
            (
                ruleset
                for ruleset in config_provision.factors
                if ruleset.apply_ruleset(selection_provision)
            ),
            None,
        )

        if validated_factor_ruleset is None:
            return None, None

        return validated_factor_ruleset.config_factor_set_id, [
            cls.config_to_selection_factor(
                val, selection_provision.selection_provision_id
            )
            for val in validated_factor_ruleset.factor_values
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        try:
            data = request.get_json()
            validated_data = cls.create_validator.dump(data)
            selection_provision = cls.schema.load(validated_data)
            db.session.add(selection_provision)

            # get factor rulesets attached to config_provision
            config_provision = (
                db.session.query(Model_ConfigProvision)
                .options(joinedload(Model_ConfigProvision.factors))
                .filter_by(config_provision_id=selection_provision.config_provision_id)
                .first()
            )

            # get the selection factor set and factor values
            factor_set_id, selection_factor_list = cls.get_first_valid_ruleset(
                config_provision, selection_provision
            )

            # if no match, clear factors and set factor set to NULL
            if selection_factor_list is None:
                selection_provision.config_factor_set_id = None
                selection_provision.factors = []
                db.session.commit()
                return {
                    "status": "success",
                    "msg": "Provision updated. No factor sets match.",
                }, 201

            # handle happy path
            # important to delete the child selection factors first, flush transaction
            # then set to the correct values
            selection_provision.config_factor_set_id = factor_set_id
            selection_provision.factors = []
            db.session.flush()

            selection_provision.factors = selection_factor_list
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(selection_provision), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    def update(cls, id, *args, **kwargs):
        try:
            data = request.get_json()
            # update the changed selection provision data, but do not commit yet
            cls._update_provision_no_commit(id, data)

            # get the updated selection_provision data from session
            # TODO: DOES THIS ACTUALLY PICK UP THE CHANGES??
            selection_provision = cls.model.find_one(
                cls.model.selection_provision_id == id
            )

            # get factor rulesets attached to config_provision
            config_provision = (
                db.session.query(Model_ConfigProvision)
                .options(joinedload(Model_ConfigProvision.factors))
                .filter_by(config_provision_id=selection_provision.config_provision_id)
                .all()
            )

            # get the selection factor set and factor values
            factor_set_id, selection_factor_list = cls.get_first_valid_ruleset(
                config_provision, selection_provision
            )

            # if no match, clear factors and set factor set to NULL
            if selection_factor_list is None:
                selection_provision.selection_factor_set_id = None
                selection_provision.factors = []
                db.session.commit()
                return {
                    "status": "success",
                    "msg": "Provision updated. No factor sets match.",
                }, 201

            # handle happy path
            # important to delete the child selection factors first, flush transaction
            # then set to the correct values
            selection_provision.selection_factor_set_id = factor_set_id
            selection_provision.factors = []
            db.session.flush()

            selection_provision.factors = selection_factor_list
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "msg": str(e)}, 400

        try:
            return cls.schema.dump(selection_provision), 201
        except Exception as e:
            return {"status": "error", "msg": str(e)}, 400

    @classmethod
    def replace(cls, id, *args, **kwargs):
        return cls.update(id, *args, **kwargs)


class CRUD_SelectionProvision_List(BaseCRUDResourceList):
    model = Model_SelectionProvision
    schema = Schema_SelectionProvision(many=True)
