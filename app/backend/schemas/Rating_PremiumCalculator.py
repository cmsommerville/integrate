from app.extensions import ma


class Schema_RatingPremiumCalculator(ma.Schema):
    
    selection_plan_id = ma.Integer()
    selection_age_band_id = ma.Integer()
    config_gender_detail_id = ma.Integer()
    config_smoker_status_detail_id = ma.Integer()
    config_relationship_detail_id = ma.Integer()
    premium_frequency_id = ma.Integer()
    face_amount_value = ma.Numeric(10,2)
    modal_premium = ma.Numeric(10,2)