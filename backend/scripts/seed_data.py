"""Seed the database with initial reference data for the National Readiness System."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.geography import FemaRegion, State, County
from app.models.hazards import HazardType
from app.models.supplies import SupplyCategory, SupplyItem
from app.models.organizations import Organization
from app.models.vendors import Vendor, VendorSupplyCapability
from app.models.contacts import Poc
from app.models.agencies import Agency, AgencySite
from app.models.it_assets import ItItemCategory, ItAsset, ItDemandForecast, ContractVehicle
from datetime import date

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        if db.query(FemaRegion).count() > 0:
            print("Database already seeded. Skipping.")
            return

        # FEMA Regions
        regions_data = [
            (1, "FEMA Region 1 - New England", "Boston", "MA"),
            (2, "FEMA Region 2 - Northeast", "New York", "NY"),
            (3, "FEMA Region 3 - Mid-Atlantic", "Philadelphia", "PA"),
            (4, "FEMA Region 4 - Southeast", "Atlanta", "GA"),
            (5, "FEMA Region 5 - Great Lakes", "Chicago", "IL"),
            (6, "FEMA Region 6 - South Central", "Denton", "TX"),
            (7, "FEMA Region 7 - Midwest", "Kansas City", "MO"),
            (8, "FEMA Region 8 - Mountain", "Denver", "CO"),
            (9, "FEMA Region 9 - Pacific Southwest", "Oakland", "CA"),
            (10, "FEMA Region 10 - Pacific Northwest", "Seattle", "WA"),
        ]
        regions = {}
        for num, name, city, st in regions_data:
            r = FemaRegion(region_number=num, region_name=name, headquarters_city=city, headquarters_state=st)
            db.add(r)
            db.flush()
            regions[num] = r

        # States (all 50 + DC + territories)
        states_data = [
            ("CT", "Connecticut", 1), ("ME", "Maine", 1), ("MA", "Massachusetts", 1),
            ("NH", "New Hampshire", 1), ("RI", "Rhode Island", 1), ("VT", "Vermont", 1),
            ("NJ", "New Jersey", 2), ("NY", "New York", 2),
            ("DC", "District of Columbia", 3), ("DE", "Delaware", 3), ("MD", "Maryland", 3),
            ("PA", "Pennsylvania", 3), ("VA", "Virginia", 3), ("WV", "West Virginia", 3),
            ("AL", "Alabama", 4), ("FL", "Florida", 4), ("GA", "Georgia", 4),
            ("KY", "Kentucky", 4), ("MS", "Mississippi", 4), ("NC", "North Carolina", 4),
            ("SC", "South Carolina", 4), ("TN", "Tennessee", 4),
            ("IL", "Illinois", 5), ("IN", "Indiana", 5), ("MI", "Michigan", 5),
            ("MN", "Minnesota", 5), ("OH", "Ohio", 5), ("WI", "Wisconsin", 5),
            ("AR", "Arkansas", 6), ("LA", "Louisiana", 6), ("NM", "New Mexico", 6),
            ("OK", "Oklahoma", 6), ("TX", "Texas", 6),
            ("IA", "Iowa", 7), ("KS", "Kansas", 7), ("MO", "Missouri", 7), ("NE", "Nebraska", 7),
            ("CO", "Colorado", 8), ("MT", "Montana", 8), ("ND", "North Dakota", 8),
            ("SD", "South Dakota", 8), ("UT", "Utah", 8), ("WY", "Wyoming", 8),
            ("AZ", "Arizona", 9), ("CA", "California", 9), ("HI", "Hawaii", 9), ("NV", "Nevada", 9),
            ("AK", "Alaska", 10), ("ID", "Idaho", 10), ("OR", "Oregon", 10), ("WA", "Washington", 10),
        ]
        states = {}
        for code, name, reg in states_data:
            s = State(state_code=code, state_name=name, fema_region_id=regions[reg].id)
            db.add(s)
            db.flush()
            states[code] = s

        # Counties (pilot set for Regions 3, 4, 6)
        counties_data = [
            ("NC", "Mecklenburg", "37119", 1155115, False, 35.2271, -80.8431),
            ("NC", "Wake", "37183", 1175025, False, 35.7796, -78.6382),
            ("NC", "New Hanover", "37129", 231214, True, 34.2257, -77.9447),
            ("NC", "Dare", "37055", 37009, True, 35.7543, -75.7583),
            ("SC", "Charleston", "45019", 424029, True, 32.7765, -79.9311),
            ("SC", "Horry", "45051", 354081, True, 33.9167, -78.8833),
            ("SC", "Richland", "45079", 429960, False, 34.0207, -80.8987),
            ("GA", "Chatham", "13051", 295291, True, 32.0809, -81.0912),
            ("GA", "Fulton", "13121", 1066710, False, 33.7490, -84.3880),
            ("GA", "Glynn", "13127", 85292, True, 31.2130, -81.4918),
            ("FL", "Miami-Dade", "12086", 2701767, True, 25.7617, -80.1918),
            ("FL", "Broward", "12011", 1944375, True, 26.1224, -80.1373),
            ("FL", "Hillsborough", "12057", 1459762, True, 27.9506, -82.4572),
            ("FL", "Duval", "12031", 995567, True, 30.3322, -81.6557),
            ("TX", "Harris", "48201", 4780913, True, 29.7604, -95.3698),
            ("TX", "Dallas", "48113", 2613539, False, 32.7767, -96.7970),
            ("TX", "Bexar", "48029", 2009324, False, 29.4241, -98.4936),
            ("TX", "Travis", "48453", 1290188, False, 30.2672, -97.7431),
            ("TX", "Cameron", "48061", 421750, True, 26.1503, -97.5039),
            ("LA", "Orleans", "22071", 383997, True, 29.9511, -90.0715),
            ("LA", "Jefferson", "22051", 440781, True, 29.8499, -90.1065),
            ("VA", "Virginia Beach city", "51810", 459470, True, 36.8529, -75.9780),
            ("VA", "Fairfax", "51059", 1150309, False, 38.8462, -77.3064),
            ("MD", "Baltimore", "24005", 854535, True, 39.4015, -76.6019),
            ("PA", "Philadelphia", "42101", 1603797, False, 39.9526, -75.1652),
        ]
        counties = {}
        for st_code, name, fips, pop, coastal, lat, lon in counties_data:
            c = County(
                state_id=states[st_code].id,
                county_name=name,
                county_fips=fips,
                population=pop,
                is_coastal=coastal,
                latitude=lat,
                longitude=lon,
            )
            db.add(c)
            db.flush()
            counties[fips] = c

        # Hazard Types
        hazard_types_data = [
            ("HURRICANE", "Hurricane / Tropical Cyclone", "tropical", "Tropical storms and hurricanes including wind, surge, and rain impacts"),
            ("FLOOD", "Inland / River Flood", "water", "River flooding, flash flooding, and coastal flooding events"),
            ("TORNADO", "Tornado", "severe_convective", "Tornado events including warnings and watches"),
            ("SEVERE_CONVECTIVE", "Severe Thunderstorm / Derecho", "severe_convective", "Severe thunderstorms, derechos, hail, and straight-line wind"),
            ("WINTER_STORM", "Winter Storm / Ice / Extreme Cold", "winter", "Blizzards, ice storms, extreme cold, and wind chill events"),
            ("HEAT", "Extreme Heat / Drought", "heat", "Heat waves, excessive heat warnings, and drought conditions"),
            ("EARTHQUAKE", "Earthquake", "geophysical", "Seismic events - rapid detection and consequence estimation only"),
            ("WILDFIRE", "Wildfire Support Conditions", "fire", "Fire weather conditions, red flag warnings, and wildfire impacts"),
        ]
        for code, name, cat, desc in hazard_types_data:
            db.add(HazardType(hazard_code=code, hazard_name=name, category=cat, description=desc))

        # Supply Categories
        supply_cats_data = [
            ("LIFE_SUSTAIN", "Life-Sustaining Commodities"),
            ("SHELTER", "Shelter & Housing"),
            ("POWER_FUEL", "Power & Fuel"),
            ("RESCUE_OPS", "Rescue & Operations"),
            ("INFRASTRUCTURE", "Infrastructure & Recovery"),
            ("PUBLIC_HEALTH", "Public Health"),
        ]
        supply_cats = {}
        for code, name in supply_cats_data:
            sc = SupplyCategory(category_code=code, category_name=name)
            db.add(sc)
            db.flush()
            supply_cats[code] = sc

        # Supply Items
        supply_items_data = [
            ("Bottled Water", "LIFE_SUSTAIN", "case"),
            ("Meals Ready to Eat", "LIFE_SUSTAIN", "meal"),
            ("Baby Supply Kit", "LIFE_SUSTAIN", "kit"),
            ("First Aid Kit", "LIFE_SUSTAIN", "kit"),
            ("Hygiene Kit", "LIFE_SUSTAIN", "kit"),
            ("Cot", "SHELTER", "unit"),
            ("Emergency Blanket", "SHELTER", "unit"),
            ("Blue Tarp", "SHELTER", "unit"),
            ("Tent", "SHELTER", "unit"),
            ("Portable Generator", "POWER_FUEL", "unit"),
            ("Diesel Fuel (gallons)", "POWER_FUEL", "gallon"),
            ("Solar Power Unit", "POWER_FUEL", "unit"),
            ("Light Tower", "POWER_FUEL", "unit"),
            ("Rescue Boat", "RESCUE_OPS", "unit"),
            ("High-Water Vehicle", "RESCUE_OPS", "unit"),
            ("Chainsaw", "RESCUE_OPS", "unit"),
            ("PPE Kit", "RESCUE_OPS", "kit"),
            ("Extraction Tool Set", "RESCUE_OPS", "set"),
            ("Water Pump", "INFRASTRUCTURE", "unit"),
            ("Sandbag", "INFRASTRUCTURE", "unit"),
            ("Dump Truck", "INFRASTRUCTURE", "unit"),
            ("Portable AC Unit", "PUBLIC_HEALTH", "unit"),
            ("Portable Heater", "PUBLIC_HEALTH", "unit"),
            ("Water Purification Unit", "PUBLIC_HEALTH", "unit"),
            ("Mobile Clinic Kit", "PUBLIC_HEALTH", "kit"),
        ]
        for item_name, cat_code, uom in supply_items_data:
            db.add(SupplyItem(
                item_name=item_name,
                supply_category_id=supply_cats[cat_code].id,
                unit_of_measure=uom,
            ))

        # IT Item Categories
        it_cats_data = [
            ("LAPTOP", "Laptop"),
            ("DESKTOP", "Desktop"),
            ("RUGGED_LAPTOP", "Rugged Laptop"),
            ("TABLET", "Tablet"),
            ("THIN_CLIENT", "Thin Client"),
            ("MONITOR", "Monitor"),
            ("DOCKING_STATION", "Docking Station"),
            ("PRINTER", "Printer / Scanner"),
            ("HOTSPOT", "Mobile Hotspot"),
            ("SAT_KIT", "Satellite Communications Kit"),
            ("SECURE_PHONE", "Secure Phone"),
            ("FIELD_TABLET", "Field / Body-Worn Tablet"),
            ("VEHICLE_COMPUTE", "Vehicle-Mounted Compute"),
            ("SERVER", "Server"),
            ("NETWORK_HW", "Networking Hardware"),
            ("UPS", "UPS Unit"),
            ("WIFI_KIT", "Secure Wi-Fi Kit"),
            ("CONTINUITY_KIT", "Disaster Recovery Workstation Kit"),
        ]
        it_cats = {}
        for code, name in it_cats_data:
            ic = ItItemCategory(category_code=code, category_name=name)
            db.add(ic)
            db.flush()
            it_cats[code] = ic

        # Organizations
        orgs_data = [
            ("FEMA Region 4", "federal_agency", "https://www.fema.gov/about/organization/region-4"),
            ("North Carolina Emergency Management", "state_agency", "https://www.ncdps.gov/our-organization/emergency-management"),
            ("South Carolina Emergency Management Division", "state_agency", "https://www.scemd.org"),
            ("Georgia Emergency Management and Homeland Security Agency", "state_agency", "https://gema.georgia.gov"),
            ("Florida Division of Emergency Management", "state_agency", "https://www.floridadisaster.org"),
            ("Texas Division of Emergency Management", "state_agency", "https://tdem.texas.gov"),
            ("Charlotte-Mecklenburg Emergency Management", "local_agency", "https://www.charlottenc.gov"),
            ("North Carolina Department of Information Technology", "state_agency", "https://www.ncdit.gov"),
            ("Trapier Water Logistics", "private_vendor", None),
            ("Sunbelt Rentals", "private_vendor", "https://www.sunbeltrentals.com"),
            ("United Rentals", "private_vendor", "https://www.unitedrentals.com"),
            ("Regional Fuel Partners", "private_vendor", None),
            ("Southeast IT Solutions", "private_vendor", None),
            ("Dell Technologies", "private_vendor", "https://www.dell.com"),
            ("HP Inc.", "private_vendor", "https://www.hp.com"),
            ("Lenovo", "private_vendor", "https://www.lenovo.com"),
        ]
        orgs = {}
        for name, otype, url in orgs_data:
            o = Organization(organization_name=name, organization_type=otype, website_url=url)
            db.add(o)
            db.flush()
            orgs[name] = o

        # Vendors
        vendors_data = [
            ("Trapier Water Logistics", "water_supplier", "NC", "FEMA Region 4", True, True, 12, 2),
            ("Sunbelt Rentals", "equipment_supplier", "NC", "Multi-state", True, True, 24, 1),
            ("United Rentals", "equipment_supplier", "GA", "National", True, True, 24, 1),
            ("Regional Fuel Partners", "fuel_supplier", "SC", "Carolinas", True, True, 8, 1),
            ("Southeast IT Solutions", "it_reseller", "NC", "Southeast", True, False, 48, 5),
            ("Dell Technologies", "it_oem", "TX", "National", True, False, 72, 7),
            ("HP Inc.", "it_oem", "CA", "National", True, False, 72, 7),
            ("Lenovo", "it_oem", "NC", "National", True, False, 72, 7),
        ]
        vendor_objs = {}
        for org_name, vtype, st, geo, contract, surge, sla, lead in vendors_data:
            v = Vendor(
                organization_id=orgs[org_name].id,
                vendor_type=vtype,
                primary_state_id=states[st].id,
                geographic_coverage=geo,
                contract_ready=contract,
                emergency_surge_capable=surge,
                response_sla_hours=sla,
                lead_time_days=lead,
            )
            db.add(v)
            db.flush()
            vendor_objs[org_name] = v

        # POCs
        pocs_data = [
            ("FEMA Region 4", "Region 4 Operations Chief", "Operations Chief", "fema_ops", "24x7", 1, None, None, 4),
            ("FEMA Region 4", "Region 4 Logistics Chief", "Logistics Chief", "fema_logistics", "24x7", 1, None, None, 4),
            ("North Carolina Emergency Management", "NC SEMA Director", "Director", "sema_leadership", "24x7", 1, "NC", None, 4),
            ("North Carolina Emergency Management", "NC Logistics Coordinator", "Logistics Coordinator", "sema_logistics", "24x7", 2, "NC", None, 4),
            ("South Carolina Emergency Management Division", "SC SEMA Director", "Director", "sema_leadership", "24x7", 1, "SC", None, 4),
            ("Georgia Emergency Management and Homeland Security Agency", "GA SEMA Director", "Director", "sema_leadership", "24x7", 1, "GA", None, 4),
            ("Florida Division of Emergency Management", "FL SEMA Director", "Director", "sema_leadership", "24x7", 1, "FL", None, 4),
            ("Texas Division of Emergency Management", "TX SEMA Director", "Director", "sema_leadership", "24x7", 1, "TX", None, 6),
            ("Charlotte-Mecklenburg Emergency Management", "Charlotte EM Director", "Emergency Manager", "local_em", "business_hours", 1, "NC", "37119", 4),
            ("North Carolina Department of Information Technology", "NC State CIO Office", "Desktop Engineering Manager", "it_owner", "business_hours", 1, "NC", None, 4),
            ("Trapier Water Logistics", "Water Logistics Lead", "Emergency Accounts Lead", "vendor_sales", "24x7", 1, "NC", None, 4),
            ("Sunbelt Rentals", "Equipment Account Lead", "Emergency Response Lead", "vendor_sales", "24x7", 1, "NC", None, 4),
            ("Southeast IT Solutions", "IT Sales Lead", "Account Executive", "vendor_sales", "business_hours", 1, "NC", None, 4),
        ]
        poc_objs = {}
        for org_name, contact, title, ctype, avail, esc, st, county_fips, reg in pocs_data:
            p = Poc(
                organization_id=orgs[org_name].id,
                contact_name=contact,
                title=title,
                contact_type=ctype,
                availability_type=avail,
                escalation_level=esc,
                state_id=states[st].id if st else None,
                county_id=counties[county_fips].id if county_fips else None,
                fema_region_id=regions[reg].id,
            )
            db.add(p)
            db.flush()
            poc_objs[contact] = p

        # Agencies
        agencies_data = [
            ("FEMA Region 4", "federal", None, None, 4, "regional_emergency_ops"),
            ("North Carolina Emergency Management", "state", "NC", None, 4, "state_emergency_management"),
            ("Charlotte-Mecklenburg Emergency Management", "local", "NC", "37119", 4, "local_emergency_management"),
            ("North Carolina Department of Information Technology", "state", "NC", None, 4, "state_it_operations"),
        ]
        agency_objs = {}
        for org_name, level, st, county_fips, reg, mission in agencies_data:
            a = Agency(
                organization_id=orgs[org_name].id,
                agency_level=level,
                state_id=states[st].id if st else None,
                county_id=counties[county_fips].id if county_fips else None,
                fema_region_id=regions[reg].id,
                mission_type=mission,
            )
            db.add(a)
            db.flush()
            agency_objs[org_name] = a

        # Agency Sites
        sites_data = [
            ("North Carolina Emergency Management", "NC State EOC", "eoc", "Raleigh", "NC", "27607", "critical", 35.7796, -78.6382),
            ("Charlotte-Mecklenburg Emergency Management", "Mecklenburg County EOC", "eoc", "Charlotte", "NC", "28202", "critical", 35.2271, -80.8431),
            ("North Carolina Department of Information Technology", "State IT Operations Center", "it_ops", "Raleigh", "NC", "27609", "high", 35.8345, -78.6219),
        ]
        site_objs = {}
        for org_name, sname, stype, city, st, postal, crit, lat, lon in sites_data:
            s = AgencySite(
                agency_id=agency_objs[org_name].id,
                site_name=sname,
                site_type=stype,
                city=city,
                state_code=st,
                postal_code=postal,
                continuity_criticality=crit,
                latitude=lat,
                longitude=lon,
            )
            db.add(s)
            db.flush()
            site_objs[sname] = s

        # IT Assets
        it_assets_data = [
            ("North Carolina Department of Information Technology", "State IT Operations Center", "NC-LT-001", "Laptop", "Dell", "Latitude 7440", "Windows 11", "2023-01-15", "2026-01-15", "active", "compliant", 4),
            ("North Carolina Department of Information Technology", "State IT Operations Center", "NC-LT-002", "Laptop", "HP", "EliteBook 840", "Windows 10", "2021-03-10", "2024-03-10", "active", "upgrade_needed", 4),
            ("North Carolina Department of Information Technology", "State IT Operations Center", "NC-DT-001", "Desktop", "Dell", "OptiPlex 7090", "Windows 11", "2022-06-01", "2025-06-01", "active", "compliant", 5),
            ("North Carolina Department of Information Technology", "State IT Operations Center", "NC-MN-001", "Monitor", "Dell", "U2722D", "N/A", "2022-06-01", "2025-06-01", "active", "compliant", 6),
            ("Charlotte-Mecklenburg Emergency Management", "Mecklenburg County EOC", "CME-TB-001", "Tablet", "Apple", "iPad Pro", "iPadOS", "2022-06-20", "2025-06-20", "active", "compliant", 3),
            ("Charlotte-Mecklenburg Emergency Management", "Mecklenburg County EOC", "CME-LT-001", "Laptop", "Lenovo", "ThinkPad X1", "Windows 11", "2023-09-01", "2026-09-01", "active", "compliant", 4),
            ("Charlotte-Mecklenburg Emergency Management", "Mecklenburg County EOC", "CME-PR-001", "Printer / Scanner", "HP", "LaserJet Pro", "N/A", "2021-01-15", "2024-01-15", "active", "compliant", 5),
            ("Charlotte-Mecklenburg Emergency Management", "Mecklenburg County EOC", "CME-HS-001", "Mobile Hotspot", "Verizon", "Jetpack", "N/A", "2024-01-01", "2026-01-01", "active", "compliant", 2),
        ]
        for org_name, site_name, tag, atype, mfr, model, osys, pdate, wdate, status, sec, lifecycle in it_assets_data:
            db.add(ItAsset(
                agency_id=agency_objs[org_name].id,
                agency_site_id=site_objs[site_name].id,
                asset_tag=tag,
                asset_type=atype,
                manufacturer=mfr,
                model=model,
                operating_system=osys,
                purchase_date=date.fromisoformat(pdate),
                warranty_end_date=date.fromisoformat(wdate),
                operating_status=status,
                security_status=sec,
                lifecycle_years=lifecycle,
            ))

        # IT Demand Forecasts
        laptop_cat = it_cats["LAPTOP"]
        hotspot_cat = it_cats["HOTSPOT"]
        printer_cat = it_cats["PRINTER"]

        db.add(ItDemandForecast(
            agency_id=agency_objs["North Carolina Emergency Management"].id,
            it_item_category_id=laptop_cat.id,
            quantity_needed=25,
            date_needed=date(2026, 6, 1),
            reason_code="continuity_refresh",
            confidence_score=0.82,
            procurement_action_score=72.5,
            notes="State EOC laptop refresh batch",
        ))
        db.add(ItDemandForecast(
            agency_id=agency_objs["Charlotte-Mecklenburg Emergency Management"].id,
            it_item_category_id=hotspot_cat.id,
            quantity_needed=15,
            date_needed=date(2026, 7, 1),
            reason_code="disaster_surge",
            confidence_score=0.76,
            procurement_action_score=68.0,
            notes="Shelter connectivity kit",
        ))
        db.add(ItDemandForecast(
            agency_id=agency_objs["North Carolina Emergency Management"].id,
            it_item_category_id=printer_cat.id,
            quantity_needed=10,
            date_needed=date(2026, 7, 1),
            reason_code="disaster_surge",
            confidence_score=0.71,
            procurement_action_score=63.0,
            notes="Field documentation support",
        ))

        # Contract Vehicles
        cv_data = [
            ("GSA MAS IT", "federal_schedule", "federal,state,local", "IT products and services", "national"),
            ("NASPO ValuePoint Computer Equipment", "cooperative", "state,local", "Computers and peripherals", "national"),
            ("NC State IT Contract", "state_contract", "state,local", "IT products", "NC"),
            ("State Emergency Procurement", "emergency", "state", "Emergency supplies", "state-level"),
            ("Local Cooperative Purchasing", "cooperative", "local", "General supplies and IT", "local"),
        ]
        for vname, vtype, buyers, cats, scope in cv_data:
            db.add(ContractVehicle(
                vehicle_name=vname,
                vehicle_type=vtype,
                eligible_buyer_types=buyers,
                categories=cats,
                jurisdiction_scope=scope,
            ))

        db.commit()
        print("Database seeded successfully!")
        print(f"  Regions: {len(regions_data)}")
        print(f"  States: {len(states_data)}")
        print(f"  Counties: {len(counties_data)}")
        print(f"  Hazard Types: {len(hazard_types_data)}")
        print(f"  Supply Categories: {len(supply_cats_data)}")
        print(f"  Supply Items: {len(supply_items_data)}")
        print(f"  IT Item Categories: {len(it_cats_data)}")
        print(f"  Organizations: {len(orgs_data)}")
        print(f"  Vendors: {len(vendors_data)}")
        print(f"  POCs: {len(pocs_data)}")
        print(f"  Agencies: {len(agencies_data)}")
        print(f"  Sites: {len(sites_data)}")
        print(f"  IT Assets: {len(it_assets_data)}")
        print(f"  Contract Vehicles: {len(cv_data)}")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
