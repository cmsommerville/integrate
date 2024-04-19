from app.extensions import db
from logger import logger
from app.shared import errors as errs
from sqlalchemy import text


SELECTION_BENEFIT_RATE = "selection_benefit_rate"


class RateEngine:
    RATING_ENGINE_PROC_NAME = "selection_rate_engine"

    def __init__(self, selection_plan_id: int, event: str):
        self.selection_plan_id = selection_plan_id
        self.event = event

    def is_valid(self):
        """
        Check if all plan data required to rate is configured
        """
        sql = text(
            """SELECT 
            (SELECT COUNT(1) FROM selection_benefit WHERE selection_plan_id = P.selection_plan_id), 
            (SELECT COUNT(1) FROM selection_provision WHERE selection_plan_id = P.selection_plan_id), 
            (SELECT COUNT(selection_value) FROM selection_provision WHERE selection_plan_id = P.selection_plan_id), 
            (SELECT COUNT(1) FROM selection_age_band WHERE selection_plan_id = P.selection_plan_id), 
            (SELECT COUNT(1) FROM selection_rating_mapper_set WHERE selection_plan_id = P.selection_plan_id),
            (SELECT COUNT(1) FROM selection_factor WHERE selection_plan_id = P.selection_plan_id)
        FROM selection_plan P
        WHERE selection_plan_id = :selection_plan_id"""
        )
        res = db.session.execute(
            sql, {"selection_plan_id": self.selection_plan_id}
        ).fetchone()
        if not res:
            raise errs.PlanInvalidError("Plan does not exist")

        bnft, prov, prov_selections, age_band, mapper_sets, factor = res
        if bnft == 0:
            raise errs.PlanInvalidError("Benefits do not exist")
        if prov == 0:
            raise errs.PlanInvalidError("Provisions do not exist")
        if prov_selections != prov:
            raise errs.PlanInvalidError("Not all provisions have been selected")
        if age_band == 0:
            raise errs.PlanInvalidError("Age bands do not exist")
        if mapper_sets == 0:
            raise errs.PlanInvalidError("Rating mappers do not exist")
        if factor == 0:
            raise errs.PlanInvalidError("Factors do not exist")

    def calculate(self):
        try:
            self.is_valid()
        except errs.PlanInvalidError:
            return
        except Exception:
            raise

        try:
            rating_sql = text(f"EXEC {self.RATING_ENGINE_PROC_NAME} :selection_plan_id")
            db.session.execute(
                rating_sql, {"selection_plan_id": self.selection_plan_id}
            )
            db.session.commit()
            logger.info(
                f"Successfully executed {self.RATING_ENGINE_PROC_NAME} for selection plan ID: {self.selection_plan_id}"
            )
        except Exception as e:
            logger.error(str(e))
            raise e
