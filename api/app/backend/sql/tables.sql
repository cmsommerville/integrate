DROP TABLE selection_benefit_rate;
CREATE TABLE selection_benefit_rate (
    selection_benefit_rate_id INTEGER IDENTITY(1, 1) PRIMARY KEY,
    selection_benefit_id INTEGER NOT NULL,
    selection_plan_id INTEGER NOT NULL,
    selection_age_band_id INTEGER NULL,
    output_attribute_detail_id1 INTEGER DEFAULT -1,
    output_attribute_detail_id2 INTEGER DEFAULT -1,
    output_attribute_detail_id3 INTEGER DEFAULT -1,
    output_attribute_detail_id4 INTEGER DEFAULT -1,
    output_attribute_detail_id5 INTEGER DEFAULT -1,
    output_attribute_detail_id6 INTEGER DEFAULT -1,
    rate_value DECIMAL(12, 5) NOT NULL,
    row_hash VARBINARY(40),
    created_dts DATETIME DEFAULT GETDATE(),
    updated_dts DATETIME DEFAULT GETDATE(),
    updated_by VARCHAR(50),
    row_eff_dts DATETIME2 GENERATED ALWAYS AS ROW START,
    row_exp_dts DATETIME2 GENERATED ALWAYS AS ROW
END,
CONSTRAINT fk_selection_benefit_rate__selection_benefit_id FOREIGN KEY (selection_benefit_id) REFERENCES selection_benefit (selection_benefit_id) ON DELETE CASCADE ON UPDATE CASCADE,
PERIOD FOR SYSTEM_TIME(row_eff_dts, row_exp_dts)
) WITH (
    SYSTEM_VERSIONING = ON (
        HISTORY_TABLE = dbo.selection_benefit_rate_history
    )
);