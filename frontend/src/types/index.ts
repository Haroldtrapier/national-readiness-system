export interface FemaRegion {
  id: string;
  region_number: number;
  region_name: string;
  headquarters_city: string | null;
  headquarters_state: string | null;
}

export interface State {
  id: string;
  state_code: string;
  state_name: string;
  fema_region_id: string | null;
  is_territory: boolean;
}

export interface County {
  id: string;
  county_name: string;
  county_fips: string | null;
  population: number | null;
  is_coastal: boolean;
  latitude: number | null;
  longitude: number | null;
}

export interface HazardSummary {
  hazard_code: string;
  hazard_name: string;
  region_number?: number;
  state_code?: string;
  county_name?: string;
  county_fips?: string;
  probability_score: number | null;
  severity_score: number | null;
  confidence_score: number | null;
  readiness_band: string;
  confidence_band?: string;
}

export interface NationalSummary {
  active_hazards: number;
  counties_at_risk: number;
  top_hazards: HazardSummary[];
  timestamp?: string;
}

export interface RegionSummary {
  region_number: number;
  region_name: string;
  active_hazards: number;
  counties_at_risk: number;
  readiness_band: string;
  hazards: HazardSummary[];
}

export interface SupplyRequirement {
  item_name: string;
  required_quantity: number;
  available_quantity: number;
  shortage_quantity: number;
  shortage_pct: number;
  priority_level: string;
}

export interface SupplyPackageItem {
  item_name: string;
  quantity: number;
}

export interface Vendor {
  id: string;
  organization_name: string;
  vendor_type: string;
  geographic_coverage: string | null;
  contract_ready: boolean;
  emergency_surge_capable: boolean;
  response_sla_hours: number | null;
  lead_time_days: number | null;
  active_status: boolean;
}

export interface VendorMatch {
  vendor_id: string;
  vendor_name: string;
  vendor_type: string;
  fit_score: number;
  contract_ready: boolean;
  emergency_surge_capable: boolean;
  response_sla_hours: number | null;
  lead_time_days: number | null;
  geographic_coverage: string | null;
}

export interface Poc {
  id: string;
  organization_name: string | null;
  contact_name: string;
  title: string | null;
  email: string | null;
  phone: string | null;
  mobile_phone: string | null;
  contact_type: string;
  availability_type: string | null;
  escalation_level: number;
  is_active: boolean;
}

export interface Agency {
  id: string;
  organization_name: string;
  agency_level: string;
  mission_type: string | null;
  active_status: boolean;
}

export interface ItAsset {
  id: string;
  asset_tag: string | null;
  asset_type: string;
  manufacturer: string | null;
  model: string | null;
  serial_number?: string | null;
  operating_system?: string | null;
  purchase_date: string | null;
  warranty_end_date: string | null;
  assigned_user?: string | null;
  operating_status: string | null;
  security_status: string | null;
  replacement_score: number | null;
}

export interface ItDemandForecast {
  id: string;
  agency_name?: string;
  item_category: string;
  quantity_needed: number;
  date_needed: string | null;
  reason_code: string;
  confidence_score: number | null;
  procurement_action_score: number | null;
  notes: string | null;
}

export interface AgencyItSummary {
  agency_id: string;
  agency_name: string;
  total_assets: number;
  expiring_warranty_90d: number;
  high_risk_replacements: number;
  surge_devices_needed: number;
  assets: ItAsset[];
  forecasts: ItDemandForecast[];
}

export interface OperationalBrief {
  title: string;
  scope: string;
  generated_at: string;
  readiness_band: string;
  threats: Array<{
    hazard_type: string;
    area: string;
    risk_level: string;
    confidence: string;
    narrative: string;
  }>;
  supply_needs: Array<{
    item_name: string;
    required: number;
    available: number;
    shortage: number;
    shortage_pct: number;
  }>;
  recommended_vendors: Array<{
    vendor_name: string;
    capability: string;
    sla_hours: number | null;
    contract_ready: boolean;
  }>;
  key_contacts: Array<{
    name: string;
    role: string;
    phone: string | null;
    email: string | null;
    availability: string | null;
  }>;
  recommended_actions: string[];
}

export type ReadinessBand = 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED' | 'BLACK';
