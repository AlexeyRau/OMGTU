ALTER TABLE clients 
ADD CONSTRAINT chk_client_type 
CHECK (client_type IN ('Физическое лицо', 'Юридическое лицо'));

ALTER TABLE clients 
ADD CONSTRAINT uniq_identity_doc UNIQUE (identity_doc);

ALTER TABLE services 
ADD CONSTRAINT uniq_service_name UNIQUE (service_name);

ALTER TABLE contracts 
ADD CONSTRAINT chk_contract_status 
CHECK (status IN ('Активен', 'Расторгнут'));

ALTER TABLE contracts 
ADD CONSTRAINT uniq_contract_number UNIQUE (contract_number);

ALTER TABLE meters 
ADD CONSTRAINT uniq_serial_number UNIQUE (serial_number);

ALTER TABLE meter_readings 
ADD CONSTRAINT chk_current_value_positive 
CHECK (current_value >= 0);

ALTER TABLE meter_readings 
ADD CONSTRAINT chk_previous_value_positive 
CHECK (previous_value >= 0);

ALTER TABLE meter_readings 
ADD CONSTRAINT chk_current_gte_previous 
CHECK (current_value >= previous_value);

ALTER TABLE meter_readings 
ADD CONSTRAINT uniq_meter_reading_date UNIQUE (meter_id, reading_date);

ALTER TABLE tariffs 
ADD CONSTRAINT chk_rate_positive 
CHECK (rate > 0);

ALTER TABLE tariffs 
ADD CONSTRAINT chk_dates_valid 
CHECK (end_date > start_date);

ALTER TABLE accruals 
ADD CONSTRAINT chk_consumption_positive 
CHECK (consumption >= 0);

ALTER TABLE accruals 
ADD CONSTRAINT chk_amount_positive 
CHECK (amount >= 0);

ALTER TABLE accruals 
ADD CONSTRAINT chk_accrual_status 
CHECK (status IN ('Не оплачено', 'Частично оплачено', 'Оплачено'));

ALTER TABLE payments 
ADD CONSTRAINT chk_payment_amount_positive 
CHECK (amount > 0);

ALTER TABLE payments 
ADD CONSTRAINT chk_payment_method 
CHECK (payment_method IN ('Карта', 'Наличные', 'Банковский перевод'));

ALTER TABLE payment_allocations 
ADD CONSTRAINT chk_allocated_amount_positive 
CHECK (allocated_amount > 0);