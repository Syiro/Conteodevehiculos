import requests
 
# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/
 
# To hit our API, you'll be making requests to:
base_url = 'https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/'
 
# Datasets are called "packages". Each package can contain many "resources"
# To retrieve the metadata for this package and its resources, use the package name in this page's URL:
url = base_url + "api/action/package_show"
params = { "id": "traffic-cameras"}
package = requests.get(url, params = params).json()
 
# To get resource data:
for idx, resource in enumerate(package["result"]["resources"]):
 
       # To download the first non datastore_active resource :
       if not resource["datastore_active"]:
           url = base_url + "datastore/dump/" + resource["id"]
           resource_dump_data = requests.get(url)