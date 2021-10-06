import json, requests

def main(dict):
    
    instanaURL = dict['instanaURL']
    
    # Filters for the queryURL
    # - size=2 we actually only expect 1 response but we limit the size to 2 to catch non-unique FQDNs (maybe a query with wildcards, etc...) 
    # - plugin=host we currently limit this function to hosts only. TBD to add other object types
    queryURL   = "/api/infrastructure-monitoring/snapshots?size=2&plugin=\"host\"&query=entity.host.fqdn:"
    dashboardURL = "/#/physical/dashboard?snapshotId="
    
    if 'fqdn' in dict:
        fqdn = dict['fqdn']
    else:
        return {'text':'FQDN not sent to function',
                'body':'FQDN not sent to function',
                'statusCode':400
                }
    
    headers = {'authorization':'apiToken ' + dict['instanaAPIToken']}
    
    currDoc = requests.get(instanaURL + queryURL + "\"" + fqdn + "\"", headers=headers)
    
    currDocJson = json.loads(currDoc.text)
    
    print (currDocJson)
    
    if len(currDocJson['items']) == 1:
        snapshotId = currDocJson['items'][0]['snapshotId']
    elif len(currDocJson['items']) == 0:
        return {'statusCode':404, 'text':'FQDN not found', 'body':'FQDN not found'}
    else:
        return {'statusCode':404, 'text':'FQDN is not unique','body':'FQDN is not unique'}
    
    return {
        'headers': { 'location': instanaURL + dashboardURL +  snapshotId },
        'statusCode': 302
    }
