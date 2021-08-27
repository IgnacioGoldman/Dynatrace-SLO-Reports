import requests, configparser, datetime, openpyxl, os
import pandas as pd

def getSLO():
	api_url = ''.join(YOUR_DT_API_URL) + '/api/v2/slo' 
	millisec_date_report = date_report.timestamp() * 1000
	millisec_date_report_end = date_report_end.timestamp() * 1000
	parameters = {
		"pageSize": 500,
		"from": int(millisec_date_report),
		"to": int(millisec_date_report_end),
		"evaluate": True
	}
	r = requests.get(api_url, headers=headers, params=parameters);
	content = r.json()
	return content

# Initialize config parser
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

#Create /data folder
if not os.path.exists('reports/'):
	os.mkdir('reports/')

# Get values from the config file
date_from = config['DATES']['From']
date_to = config['DATES']['To']

# Name of the report 
string_date = date_from+"-to-"+date_to

# Iterate though tenants
tenant_count=1
for (tenantkey, val) in config.items('TENANTS'):
	# Get tenant URL and TOKEN
	YOUR_DT_API_URL = val.split(" ")[0].rstrip('\n')
	YOUR_DT_API_TOKEN = val.split(" ")[1].rstrip('\n')

	# Format date
	date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
	date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
	
	# Create header
	headers={}
	headers["Authorization"] = "Api-Token "+YOUR_DT_API_TOKEN

	#Generate env_id
	if "/e/" in YOUR_DT_API_URL:
		env_id = YOUR_DT_API_URL.split("/e/")[1]
	else:
		env_id = YOUR_DT_API_URL.split("//")[1]

	#Create tenant folder
	path = "reports/"+env_id
	if not os.path.exists(path):
		os.mkdir(path)

	# Iterate to get results per day 
	date_report = date_from
	print("Getting SLO for tenant "+env_id)
	writer = pd.ExcelWriter(path+"/"+string_date+'.xlsx')
	while (date_report<=date_to):
		date_report_end = date_report + datetime.timedelta(hours=24) 
		
		# Get data from Dynatrace
		content = getSLO()

		# Create pandas
		df = pd.json_normalize(content['slo'])
		
		# Save to excel file/sheet	
		df.to_excel(writer, sheet_name=str(date_report).split(" ")[0])
	
		date_report = date_report + datetime.timedelta(hours=24)
	writer.save()
	tenant_count+=1