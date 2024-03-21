
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Fetch the list of GCP regions and the cheapest VM instance type for each region from the Cloud API
@app.route('/')
def index():
    url = 'https://compute.googleapis.com/compute/v1/projects/YOUR_PROJECT_ID/zones'
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
    response = requests.get(url, headers=headers)
    data = response.json()
    regions = data['items']

    cheapest_instances = {}
    for region in regions:
        zone = region['name']
        url = f'https://compute.googleapis.com/compute/v1/projects/YOUR_PROJECT_ID/zones/{zone}/machineTypes'
        response = requests.get(url, headers=headers)
        data = response.json()
        machine_types = data['items']

        cheapest_instance = None
        cheapest_price = None
        for machine_type in machine_types:
            if machine_type['name'] in ['e2-standard-4', 'n2-standard-4', 'n2-standard-8', 'n2-standard-16', 'n2-standard-32', 'n2d-standard-4', 'n2d-standard-8', 'n2d-standard-16', 'n2d-standard-32']:
                price = float(machine_type['guestCpus']) * float(machine_type['pricePerCoreHour'])
                if cheapest_price is None or price < cheapest_price:
                    cheapest_instance = machine_type['name']
                    cheapest_price = price

        cheapest_instances[region['name']] = {
            'instance_type': cheapest_instance,
            'price': cheapest_price
        }

    return render_template('index.html', regions=regions, cheapest_instances=cheapest_instances)

# Provide an interface for external systems to access the application's data
@app.route('/api/instances')
def api_instances():
    url = 'https://compute.googleapis.com/compute/v1/projects/YOUR_PROJECT_ID/zones'
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
    response = requests.get(url, headers=headers)
    data = response.json()
    regions = data['items']

    cheapest_instances = {}
    for region in regions:
        zone = region['name']
        url = f'https://compute.googleapis.com/compute/v1/projects/YOUR_PROJECT_ID/zones/{zone}/machineTypes'
        response = requests.get(url, headers=headers)
        data = response.json()
        machine_types = data['items']

        cheapest_instance = None
        cheapest_price = None
        for machine_type in machine_types:
            if machine_type['name'] in ['e2-standard-4', 'n2-standard-4', 'n2-standard-8', 'n2-standard-16', 'n2-standard-32', 'n2d-standard-4', 'n2d-standard-8', 'n2d-standard-16', 'n2d-standard-32']:
                price = float(machine_type['guestCpus']) * float(machine_type['pricePerCoreHour'])
                if cheapest_price is None or price < cheapest_price:
                    cheapest_instance = machine_type['name']
                    cheapest_price = price

        cheapest_instances[region['name']] = {
            'instance_type': cheapest_instance,
            'price': cheapest_price
        }

    return jsonify(cheapest_instances)

# Handle POST requests to check if a new region has been added to GCP
@app.route('/region-checker', methods=['POST'])
def region_checker():
    url = 'https://compute.googleapis.com/compute/v1/projects/YOUR_PROJECT_ID/zones'
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
    response = requests.get(url, headers=headers)
    data = response.json()
    regions = data['items']

    new_regions = []
    for region in regions:
        if region['name'] not in cheapest_instances:
            new_regions.append(region['name'])

    if len(new_regions) > 0:
        # Update the application's internal data
        cheapest_instances.update(get_cheapest_instances(new_regions))

    return jsonify(new_regions)

if __name__ == '__main__':
    app.run(debug=True)
