const API_BASE = '/api/v1';

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  geography: {
    getRegions: () => fetchJson<any[]>('/geography/regions'),
    getStates: (regionNumber?: number) =>
      fetchJson<any[]>(`/geography/states${regionNumber ? `?region_number=${regionNumber}` : ''}`),
    getCounties: (stateCode?: string) =>
      fetchJson<any[]>(`/geography/counties${stateCode ? `?state_code=${stateCode}` : ''}`),
  },

  hazards: {
    getNationalSummary: () => fetchJson<any>('/hazards/national-summary'),
    getRegionHazards: (regionNumber: number) => fetchJson<any>(`/hazards/regions/${regionNumber}`),
    getStateHazards: (stateCode: string) => fetchJson<any>(`/hazards/states/${stateCode}`),
    getCountyHazards: (countyFips: string) => fetchJson<any>(`/hazards/counties/${countyFips}`),
    refresh: () => fetch(`${API_BASE}/hazards/refresh`, { method: 'POST' }).then(r => r.json()),
  },

  readiness: {
    getNational: () => fetchJson<any>('/readiness/national'),
    getRegion: (regionNumber: number) => fetchJson<any>(`/readiness/regions/${regionNumber}`),
    getState: (stateCode: string) => fetchJson<any>(`/readiness/states/${stateCode}`),
    getCounty: (countyFips: string) => fetchJson<any>(`/readiness/counties/${countyFips}`),
  },

  supplies: {
    getCatalog: () => fetchJson<any>('/supplies/catalog'),
    getPackages: (hazardCode: string, severityBand?: string) =>
      fetchJson<any>(`/supplies/packages/${hazardCode}${severityBand ? `?severity_band=${severityBand}` : ''}`),
    getRequirements: (countyFips: string) => fetchJson<any>(`/supplies/requirements/${countyFips}`),
  },

  vendors: {
    getAll: () => fetchJson<any[]>('/vendors'),
    matchSupply: (itemName: string, stateCode?: string) =>
      fetchJson<any>(`/vendors/matches/supply?item_name=${itemName}${stateCode ? `&state_code=${stateCode}` : ''}`),
    getByRegion: (regionNumber: number) => fetchJson<any[]>(`/vendors/by-region/${regionNumber}`),
  },

  pocs: {
    getFema: (regionNumber: number) => fetchJson<any[]>(`/pocs/fema/${regionNumber}`),
    getSema: (stateCode: string) => fetchJson<any[]>(`/pocs/sema/${stateCode}`),
    getLocal: (countyFips: string) => fetchJson<any[]>(`/pocs/local/${countyFips}`),
    getAll: (contactType?: string, stateCode?: string) => {
      const params = new URLSearchParams();
      if (contactType) params.set('contact_type', contactType);
      if (stateCode) params.set('state_code', stateCode);
      return fetchJson<any[]>(`/pocs/all?${params}`);
    },
  },

  agencies: {
    getAll: (level?: string, stateCode?: string) => {
      const params = new URLSearchParams();
      if (level) params.set('level', level);
      if (stateCode) params.set('state_code', stateCode);
      return fetchJson<any[]>(`/agencies?${params}`);
    },
    getById: (agencyId: string) => fetchJson<any>(`/agencies/${agencyId}`),
  },

  itAssets: {
    getAgencyAssets: (agencyId: string) => fetchJson<any>(`/it-assets/agencies/${agencyId}`),
    getStateForecast: (stateCode: string) => fetchJson<any>(`/it-assets/forecast/states/${stateCode}`),
    getRegionForecast: (regionNumber: number) => fetchJson<any>(`/it-assets/forecast/regions/${regionNumber}`),
  },

  briefs: {
    getNational: () => fetchJson<any>('/briefs/national'),
    getRegion: (regionNumber: number) => fetchJson<any>(`/briefs/region/${regionNumber}`),
  },
};
