# National Readiness, Supply & Public Sector Equipment Intelligence System

An AI-powered operational platform that tracks national weather hazards, predicts disaster impacts by region, maps required supplies and vendors, routes FEMA/SEMA points of contact, and tracks government IT equipment demand for federal, state, and local agencies.

## System Modules

### 1. Disaster Readiness Command
- Real-time hazard ingestion from NWS alerts, USGS earthquake feeds
- Probabilistic risk scoring by county, state, and FEMA region
- Readiness band classification (GREEN / YELLOW / ORANGE / RED / BLACK)
- Hazard-to-supply mapping with quantity recommendations
- Vendor matching and fit scoring
- FEMA/SEMA/local POC routing
- Operational brief generation

### 2. Government IT Equipment Demand Command
- Federal, state, and local IT asset lifecycle tracking
- Warranty expiration and replacement scoring
- Disaster-driven IT surge forecasting
- Contract vehicle matching (GSA MAS, NASPO, state contracts)
- Vendor capability and fulfillment matching
- Buyer and procurement POC routing

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        React Dashboard                          │
│  National │ Region │ State │ County │ IT │ Vendors │ POCs │ Briefs│
├──────────────────────────────────────────────────────────────────┤
│                        FastAPI Backend                          │
│  Hazards │ Readiness │ Supplies │ Vendors │ POCs │ IT Assets    │
├──────────────────────────────────────────────────────────────────┤
│                    Services & Scoring Engine                     │
│  Ingestion │ Scoring │ Supply Planning │ Vendor Match │ Briefs  │
├──────────────────────────────────────────────────────────────────┤
│                    SQLite / PostgreSQL + PostGIS                 │
└──────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python scripts/seed_data.py
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

## API Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| Geography | `GET /api/v1/geography/regions` | List FEMA regions |
| Geography | `GET /api/v1/geography/states` | List states |
| Geography | `GET /api/v1/geography/counties` | List counties |
| Hazards | `GET /api/v1/hazards/national-summary` | National hazard overview |
| Hazards | `GET /api/v1/hazards/regions/{n}` | Region hazards |
| Hazards | `GET /api/v1/hazards/states/{code}` | State hazards |
| Hazards | `POST /api/v1/hazards/refresh` | Ingest latest NWS/USGS feeds |
| Readiness | `GET /api/v1/readiness/national` | National readiness scores |
| Readiness | `GET /api/v1/readiness/regions/{n}` | Region readiness |
| Supplies | `GET /api/v1/supplies/catalog` | Supply item catalog |
| Supplies | `GET /api/v1/supplies/packages/{code}` | Supply packages by hazard |
| Supplies | `GET /api/v1/supplies/requirements/{fips}` | County supply requirements |
| Vendors | `GET /api/v1/vendors` | All vendors |
| Vendors | `GET /api/v1/vendors/matches/supply` | Vendor matching |
| POCs | `GET /api/v1/pocs/fema/{n}` | FEMA region contacts |
| POCs | `GET /api/v1/pocs/sema/{code}` | State EM contacts |
| POCs | `GET /api/v1/pocs/local/{fips}` | Local contacts |
| IT Assets | `GET /api/v1/it-assets/agencies/{id}` | Agency IT summary |
| IT Assets | `GET /api/v1/it-assets/forecast/states/{code}` | State IT forecast |
| Briefs | `GET /api/v1/briefs/national` | National operational brief |
| Briefs | `GET /api/v1/briefs/region/{n}` | Region operational brief |

## Dashboard Pages

1. **National Command** - U.S. hazard map, top threats, supply gaps, metrics
2. **FEMA Region Operations** - Region-specific hazards, county risk table, contacts, vendors
3. **State Operations** - State-level hazards, county breakdown, IT forecasts
4. **County Operations** - County hazards, supply requirements, local contacts
5. **Agency IT Command** - Asset inventory, lifecycle charts, demand forecasts
6. **Vendor Operations** - Vendor directory, capacity, contract readiness
7. **POC Command Center** - Contact directory with filters and escalation
8. **Operational Briefs** - Generated intelligence reports with action packages

## Hazard Modules

| Module | Sources | Forecast Type |
|--------|---------|---------------|
| Hurricane/Tropical | NWS, NHC | Probabilistic |
| Flood | NWS, NWPS | Probabilistic |
| Tornado/Severe | NWS, SPC | Probabilistic |
| Winter Storm | NWS | Probabilistic |
| Heat/Drought | NWS, CPC | Probabilistic |
| Earthquake | USGS | Detection + Consequence |
| Wildfire | NWS | Probabilistic |

## Risk Scoring

```
Hazard Score = (Probability × 0.30 + Severity × 0.25 + Exposure × 0.20
              + Vulnerability × 0.15 + Confidence × 0.10) × 10
```

| Band | Score | Action |
|------|-------|--------|
| GREEN | < 30 | Monitor |
| YELLOW | 30-49 | Preparedness Review |
| ORANGE | 50-69 | Stage Resources |
| RED | 70-84 | Activate / Deploy |
| BLACK | 85+ | Catastrophic Multi-State Support |

## Data Sources

- [NWS API](https://api.weather.gov) - Forecasts, alerts, observations
- [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1) - Real-time seismic events
- FEMA Regions - Federal operating structure
- GSA MAS IT - Federal IT procurement
- NASPO ValuePoint - State cooperative purchasing

## Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (dev) / PostgreSQL + PostGIS (production)
- **Deployment**: Vercel (frontend), any Python host (backend)

## Pilot Scope

- FEMA Regions 3, 4, 6
- States: NC, SC, GA, FL, TX, LA, VA, MD, PA
- 25 pilot counties
- 8 vendors (emergency + IT)
- 13 POCs across FEMA, SEMA, local, IT, vendors
- 4 agencies with sites
- 8 IT assets with lifecycle tracking
- 5 contract vehicles
