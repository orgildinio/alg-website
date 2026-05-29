#!/usr/bin/env python3
"""Geocode all 73 locator records using Nominatim (1 req/sec rate limit).
Outputs public/data/local_support.json with lat/lon baked in.
"""
import json, time, urllib.request, urllib.parse, sys

INPUT = '/home/ubuntu/upload/active_locator_data.json'
OUTPUT = 'public/data/local_support.json'

with open(INPUT) as f:
    data = json.load(f)

HEADERS = {'User-Agent': 'ALGWebsite/1.0 (james@archipelagolighting.com)'}

def geocode(city, state, country):
    if not city:
        # No city — use state centroid via state-only query
        q = f"{state}, {country}"
    else:
        city_clean = city.strip().rstrip(',')
        q = f"{city_clean}, {state}, {country}"
    
    params = urllib.parse.urlencode({
        'q': q,
        'format': 'json',
        'limit': 1,
        'addressdetails': 0,
    })
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            results = json.loads(resp.read())
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
    return None, None

def process_layer(records, layer_name):
    out = []
    for i, rec in enumerate(records):
        city = rec.get('city') or ''
        state = rec.get('state', '')
        country = rec.get('country', 'USA')
        # Normalize country
        if country in ('U.S.A', 'U.S.A.', 'USA', 'US'):
            country = 'USA'
        
        print(f"  [{i+1}/{len(records)}] {rec['name']} — {city}, {state}")
        lat, lon = geocode(city, state, country)
        if lat is None:
            print(f"    !! FAILED geocode for {rec['name']}", file=sys.stderr)
        else:
            print(f"    → {lat:.4f}, {lon:.4f}")
        
        entry = dict(rec)
        entry['lat'] = lat
        entry['lon'] = lon
        out.append(entry)
        time.sleep(1.1)  # Nominatim 1 req/sec
    return out

import os
os.makedirs('public/data', exist_ok=True)

print("=== Geocoding Sales Reps ===")
reps = process_layer(data['sales_reps'], 'sales_reps')

print("\n=== Geocoding Distributors ===")
dists = process_layer(data['distributors'], 'distributors')

print("\n=== Geocoding Warehouses ===")
whs = process_layer(data['warehouses'], 'warehouses')

output = {
    '_meta': data['_meta'],
    'sales_reps': reps,
    'distributors': dists,
    'warehouses': whs,
}
output['_meta']['geocoded_at'] = time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime())
output['_meta']['geocoding'] = 'Nominatim (OSM) — city+state+country query'

with open(OUTPUT, 'w') as f:
    json.dump(output, f, indent=2)

# Summary
failed = sum(1 for r in reps + dists + whs if r['lat'] is None)
print(f"\n✅ Done. {len(reps)+len(dists)+len(whs)} records geocoded. {failed} failed.")
print(f"Output: {OUTPUT}")
