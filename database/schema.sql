-- National Readiness, Supply & Public Sector Equipment Intelligence System
-- PostgreSQL Schema v1

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================================================
-- Geography / Reference Tables
-- =========================================================

CREATE TABLE fema_regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_number INTEGER NOT NULL UNIQUE CHECK (region_number BETWEEN 1 AND 10),
    region_name TEXT NOT NULL,
    headquarters_city TEXT,
    headquarters_state TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_code CHAR(2) NOT NULL UNIQUE,
    state_name TEXT NOT NULL UNIQUE,
    fema_region_id UUID REFERENCES fema_regions(id) ON DELETE SET NULL,
    is_territory BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE counties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_id UUID NOT NULL REFERENCES states(id) ON DELETE CASCADE,
    county_name TEXT NOT NULL,
    county_fips VARCHAR(5) UNIQUE,
    population BIGINT,
    is_coastal BOOLEAN NOT NULL DEFAULT FALSE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_counties_state_id ON counties(state_id);
CREATE INDEX idx_counties_fips ON counties(county_fips);

-- =========================================================
-- Hazard Tables
-- =========================================================

CREATE TABLE hazard_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hazard_code TEXT NOT NULL UNIQUE,
    hazard_name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE hazard_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hazard_type_id UUID NOT NULL REFERENCES hazard_types(id),
    event_source TEXT NOT NULL,
    external_event_id TEXT,
    event_name TEXT,
    event_status TEXT DEFAULT 'active',
    probability_score DOUBLE PRECISION,
    severity_score DOUBLE PRECISION,
    confidence_score DOUBLE PRECISION,
    issued_at TIMESTAMPTZ,
    start_at TIMESTAMPTZ,
    end_at TIMESTAMPTZ,
    source_payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_hazard_events_type ON hazard_events(hazard_type_id);
CREATE INDEX idx_hazard_events_status ON hazard_events(event_status);
CREATE INDEX idx_hazard_events_external ON hazard_events(external_event_id);

CREATE TABLE county_hazard_impacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    county_id UUID NOT NULL REFERENCES counties(id),
    hazard_event_id UUID NOT NULL REFERENCES hazard_events(id),
    probability_score DOUBLE PRECISION NOT NULL,
    severity_score DOUBLE PRECISION NOT NULL,
    exposure_score DOUBLE PRECISION,
    vulnerability_score DOUBLE PRECISION,
    hazard_score DOUBLE PRECISION,
    readiness_band TEXT,
    confidence_band TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_county_impacts_county ON county_hazard_impacts(county_id);
CREATE INDEX idx_county_impacts_event ON county_hazard_impacts(hazard_event_id);
CREATE INDEX idx_county_impacts_band ON county_hazard_impacts(readiness_band);

CREATE TABLE readiness_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    county_id UUID REFERENCES counties(id),
    state_id UUID REFERENCES states(id),
    fema_region_id UUID REFERENCES fema_regions(id),
    hazard_event_id UUID REFERENCES hazard_events(id),
    readiness_band TEXT NOT NULL,
    hazard_score DOUBLE PRECISION NOT NULL,
    confidence_band TEXT,
    action_window TEXT,
    narrative TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================================================
-- Supply Tables
-- =========================================================

CREATE TABLE supply_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_code TEXT NOT NULL UNIQUE,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE supply_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku_code TEXT UNIQUE,
    item_name TEXT NOT NULL UNIQUE,
    supply_category_id UUID REFERENCES supply_categories(id),
    unit_of_measure TEXT NOT NULL,
    item_description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE supply_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hazard_code TEXT NOT NULL,
    severity_band TEXT NOT NULL,
    package_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE supply_package_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supply_package_id UUID NOT NULL REFERENCES supply_packages(id),
    supply_item_id UUID NOT NULL REFERENCES supply_items(id),
    default_quantity INTEGER NOT NULL,
    notes TEXT
);

CREATE TABLE supply_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    readiness_assessment_id UUID NOT NULL REFERENCES readiness_assessments(id),
    supply_item_id UUID NOT NULL REFERENCES supply_items(id),
    required_quantity DOUBLE PRECISION NOT NULL,
    available_quantity DOUBLE PRECISION,
    shortage_quantity DOUBLE PRECISION,
    priority_level TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================================================
-- Organization / Vendor Tables
-- =========================================================

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    website_url TEXT,
    sam_uei TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE vendors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    vendor_type TEXT NOT NULL,
    primary_state_id UUID REFERENCES states(id),
    geographic_coverage TEXT,
    contract_ready BOOLEAN NOT NULL DEFAULT FALSE,
    emergency_surge_capable BOOLEAN NOT NULL DEFAULT FALSE,
    response_sla_hours INTEGER,
    lead_time_days INTEGER,
    past_performance_notes TEXT,
    active_status BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE vendor_supply_capabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id UUID NOT NULL REFERENCES vendors(id),
    supply_item_id UUID REFERENCES supply_items(id),
    it_item_category_id UUID,
    item_type TEXT NOT NULL,
    daily_capacity INTEGER,
    weekly_capacity INTEGER,
    unit_of_measure TEXT,
    service_regions JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE vendor_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_type TEXT NOT NULL,
    supply_requirement_id UUID REFERENCES supply_requirements(id),
    it_demand_forecast_id UUID,
    vendor_id UUID NOT NULL REFERENCES vendors(id),
    fit_score DOUBLE PRECISION NOT NULL,
    delivery_risk_score DOUBLE PRECISION,
    ranking_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================================================
-- Contact Tables
-- =========================================================

CREATE TABLE pocs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    contact_name TEXT NOT NULL,
    title TEXT,
    email TEXT,
    phone TEXT,
    mobile_phone TEXT,
    contact_type TEXT NOT NULL,
    availability_type TEXT,
    escalation_level INTEGER NOT NULL DEFAULT 1,
    state_id UUID REFERENCES states(id),
    county_id UUID REFERENCES counties(id),
    fema_region_id UUID REFERENCES fema_regions(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pocs_type ON pocs(contact_type);
CREATE INDEX idx_pocs_region ON pocs(fema_region_id);
CREATE INDEX idx_pocs_state ON pocs(state_id);

-- =========================================================
-- Agency Tables
-- =========================================================

CREATE TABLE agencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    agency_level TEXT NOT NULL,
    state_id UUID REFERENCES states(id),
    county_id UUID REFERENCES counties(id),
    fema_region_id UUID REFERENCES fema_regions(id),
    mission_type TEXT,
    procurement_owner_poc_id UUID REFERENCES pocs(id),
    emergency_owner_poc_id UUID REFERENCES pocs(id),
    it_owner_poc_id UUID REFERENCES pocs(id),
    active_status BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE agency_sites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(id),
    site_name TEXT NOT NULL,
    site_type TEXT NOT NULL,
    address_line_1 TEXT,
    city TEXT,
    state_code CHAR(2),
    postal_code TEXT,
    county_name TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    continuity_criticality TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================================================
-- IT Asset Tables
-- =========================================================

CREATE TABLE it_item_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_code TEXT NOT NULL UNIQUE,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE it_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(id),
    agency_site_id UUID REFERENCES agency_sites(id),
    asset_tag TEXT,
    asset_type TEXT NOT NULL,
    manufacturer TEXT,
    model TEXT,
    serial_number TEXT,
    operating_system TEXT,
    purchase_date DATE,
    warranty_end_date DATE,
    assigned_user TEXT,
    operating_status TEXT,
    security_status TEXT,
    lifecycle_years INTEGER,
    replacement_score DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_it_assets_agency ON it_assets(agency_id);
CREATE INDEX idx_it_assets_type ON it_assets(asset_type);

CREATE TABLE it_demand_forecasts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(id),
    county_id UUID REFERENCES counties(id),
    linked_hazard_event_id UUID REFERENCES hazard_events(id),
    it_item_category_id UUID NOT NULL REFERENCES it_item_categories(id),
    quantity_needed INTEGER NOT NULL,
    date_needed DATE,
    reason_code TEXT NOT NULL,
    confidence_score DOUBLE PRECISION,
    procurement_action_score DOUBLE PRECISION,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE contract_vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_name TEXT NOT NULL,
    vehicle_type TEXT NOT NULL,
    eligible_buyer_types TEXT,
    categories TEXT,
    jurisdiction_scope TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE agency_contract_eligibility (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(id),
    contract_vehicle_id UUID NOT NULL REFERENCES contract_vehicles(id),
    eligibility_status TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add foreign key for vendor_supply_capabilities.it_item_category_id
ALTER TABLE vendor_supply_capabilities
    ADD CONSTRAINT fk_vendor_supply_it_cat
    FOREIGN KEY (it_item_category_id) REFERENCES it_item_categories(id);

-- Add foreign key for vendor_matches.it_demand_forecast_id
ALTER TABLE vendor_matches
    ADD CONSTRAINT fk_vendor_match_forecast
    FOREIGN KEY (it_demand_forecast_id) REFERENCES it_demand_forecasts(id);
