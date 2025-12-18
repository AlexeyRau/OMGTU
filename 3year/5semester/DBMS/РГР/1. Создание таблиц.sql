-- 1. Таблица клиентов
CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    client_type VARCHAR(20) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    identity_doc VARCHAR(100) NOT NULL,
    contacts TEXT NOT NULL
);

-- 2. Таблица услуг
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

-- 3. Таблица договоров
CREATE TABLE contracts (
    contract_id SERIAL PRIMARY KEY,
    contract_number VARCHAR(50) NOT NULL,
    client_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Активен',
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE RESTRICT
);

-- 4. Таблица счетчиков
CREATE TABLE meters (
    meter_id SERIAL PRIMARY KEY,
    serial_number VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    installation_date DATE NOT NULL,
    location TEXT NOT NULL,
    contract_id INTEGER NOT NULL,
    FOREIGN KEY (contract_id) REFERENCES contracts(contract_id) ON DELETE CASCADE
);

-- 5. Таблица показаний счетчиков
CREATE TABLE meter_readings (
    reading_id SERIAL PRIMARY KEY,
    meter_id INTEGER NOT NULL,
    reading_date DATE NOT NULL,
    current_value DECIMAL(15, 3) NOT NULL,
    previous_value DECIMAL(15, 3) NOT NULL,
    consumption DECIMAL(15, 3) GENERATED ALWAYS AS (current_value - previous_value) STORED,
    FOREIGN KEY (meter_id) REFERENCES meters(meter_id) ON DELETE CASCADE
);

-- 6. Таблица тарифов
CREATE TABLE tariffs (
    tariff_id SERIAL PRIMARY KEY,
    service_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    rate DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE
);

-- 7. Таблица начислений
CREATE TABLE accruals (
    accrual_id SERIAL PRIMARY KEY,
    contract_id INTEGER NOT NULL,
    period DATE NOT NULL,
    consumption DECIMAL(15, 3) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Не оплачено',
    FOREIGN KEY (contract_id) REFERENCES contracts(contract_id) ON DELETE CASCADE
);

-- 8. Таблица платежей
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    amount DECIMAL(15, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
);

-- 9. Таблица распределения платежей
CREATE TABLE payment_allocations (
    allocation_id SERIAL PRIMARY KEY,
    payment_id INTEGER NOT NULL,
    accrual_id INTEGER NOT NULL,
    allocated_amount DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (payment_id) REFERENCES payments(payment_id) ON DELETE CASCADE,
    FOREIGN KEY (accrual_id) REFERENCES accruals(accrual_id) ON DELETE CASCADE
);