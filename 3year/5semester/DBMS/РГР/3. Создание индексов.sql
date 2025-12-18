CREATE INDEX idx_contracts_client_id ON contracts(client_id);
CREATE INDEX idx_contracts_service_id ON contracts(service_id);
CREATE INDEX idx_meters_contract_id ON meters(contract_id);
CREATE INDEX idx_meter_readings_meter_id ON meter_readings(meter_id);
CREATE INDEX idx_tariffs_service_id ON tariffs(service_id);
CREATE INDEX idx_accruals_contract_id ON accruals(contract_id);
CREATE INDEX idx_payments_client_id ON payments(client_id);
CREATE INDEX idx_payment_allocations_payment_id ON payment_allocations(payment_id);
CREATE INDEX idx_payment_allocations_accrual_id ON payment_allocations(accrual_id);

-- Для быстрого поиска клиентов по документу
CREATE INDEX idx_clients_identity_doc ON clients(identity_doc);

-- Для поиска договоров по номеру
CREATE INDEX idx_contracts_contract_number ON contracts(contract_number);

-- Для поиска счётчиков по серийному номеру
CREATE INDEX idx_meters_serial_number ON meters(serial_number);

-- Для временных диапазонов в показаниях и начислениях
CREATE INDEX idx_meter_readings_reading_date ON meter_readings(reading_date);
CREATE INDEX idx_accruals_period ON accruals(period);
CREATE INDEX idx_accruals_status ON accruals(status);
CREATE INDEX idx_payments_payment_date ON payments(payment_date);

-- Для поиска тарифов по периоду действия
CREATE INDEX idx_tariffs_dates ON tariffs(start_date, end_date);