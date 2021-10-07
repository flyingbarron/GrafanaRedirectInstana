
import json, requests

def main(dict):
    
    instanaURL = dict['instanaURL']
    
    # Filters for the queryURL
    # - size=2 we actually only expect 1 response but we limit the size to 2 to catch non-unique FQDNs (maybe a query with wildcards, etc...) 
    # - plugin=host we currently limit this function to hosts only. TBD to add other object types
    baseQueryURL   = "/api/infrastructure-monitoring/snapshots?size=999&"
    dashboardURL = "/#/physical/dashboard?snapshotId="
    headers = {'authorization':'apiToken ' + dict['instanaAPIToken']}
    fqdnQueryURL = baseQueryURL + "plugin=\"host\"&query=entity.host.fqdn:\""

    print (dict) 
    try:
        if 'fqdn' in dict:
            fqdn = dict['fqdn']
            queryURL = baseQueryURL + fqdnQueryURL + fqdn + "\""
            entityResponse = requests.get(instanaURL + queryURL, headers=headers).json()
    
        elif 'python_name' in dict: # We need to find the precise hostname for this Python app
            pythonAppName = dict['python_name'].split()[0]
            fqdn = dict['python_name'].split()[3].replace('"','').replace(')','')
            queryURL = baseQueryURL + fqdnQueryURL + fqdn + "\""
            fqdnResponse = requests.get(instanaURL + queryURL, headers=headers).json()
            fqdnId = fqdnResponse['items'][0]['host']
            queryURL = baseQueryURL + "plugin=\"pythonRuntimePlatform\"&query=entity.python.app.name:\"" + pythonAppName + "\""
            entityResponseList = requests.get(instanaURL + queryURL, headers=headers).json()
            for i in entityResponseList['items']:
                if i['host'] == fqdnId:
                    snapshotId = i['snapshotId']
            return {
                'headers': { 'location': instanaURL + dashboardURL +  snapshotId },
                'statusCode': 302
            }
    
        else:
            return {'text':'No valid entity sent to function',
                    'body':'No valid entity sent to function',
                    'statusCode':400
                    }
                    
        print (queryURL)
        
        if len(entityResponse['items']) == 1:
            snapshotId = entityResponse['items'][0]['snapshotId']
        elif len(entityResponse['items']) == 0:
            return {'statusCode':404, 'text':'entity not found', 'body':'entity not found'}
        else:
            return {'statusCode':404, 'text':'entity is not unique','body':'entity is not unique'}
        
        return {
            'headers': { 'location': instanaURL + dashboardURL +  snapshotId },
            'statusCode': 302
        }
        
    except errorMsg:
        return {
            'body':'Error redirecting to Instana',
            'text':'Error redirecting to Instana',
            'statusCode': 503
        }
            
