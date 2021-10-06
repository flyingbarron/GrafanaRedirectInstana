# Grafana redirect to Instana
A helper function to redirect Grafana drill down links into Instana

The purpose of this function is to extend the Instana plugin for Grafana and add a new feature - drill down from a Grafana graph to the Instana object dashboard.

## The problem

The current problem is that an Instana dashboard URL requires the snapshotId of the object, which is not known by Grafana. The timeseries Grafana collects from Instana only has the object name (FQDN in the case of hosts).

> Note that as of October 2021, this function only works on objects of type `host`

An example of a dashboard URL is `https://<instanaHostURL>/#/physical/dashboard?snapshotId=<snapshotId>`

After setting up the Grafana plugin for Instana (per https://grafana.com/grafana/plugins/instana-datasource/) you can create Grafana dashboards which show information about hosts monitored by Instana.

![image](https://user-images.githubusercontent.com/7903045/136160956-7492e686-5487-4269-8ddf-2107a12b7961.png)

You can now edit your widget to add a drill down link:

<img width="181" alt="image" src="https://user-images.githubusercontent.com/7903045/136161243-8d0a2afc-086e-4777-ba24-36046fb66066.png">

Scroll to the bottom of the sidebar and click "Add link" in Data links.

<img src="https://user-images.githubusercontent.com/7903045/136161610-1c9880a4-43f5-42ec-8c30-15db8c3fb819.png" width="300" >


What we would like to do now is add a link in the format of `https://<instanaHostURL>/#/physical/dashboard?snapshotId=<snapshotId>`

But as you can see, `snapshotId` is not one of the available fields:

<img width="791" alt="image" src="https://user-images.githubusercontent.com/7903045/136162134-b16b6348-a707-40ed-90cc-bb3a08103ef7.png">

The solution is to create a helper function which will recieve the `Series Name` (in the case of hosts this is the FQDN), translate that to the most recent snapshotId and redirect the browser to the Instana server.

The code shared in this repository does this.

## The solution

The solution assumes that it will receive 3 parameters:
1. instanaURL - the base URL of the Instana backend (`https://myInstanaserver`)
2. instanaAPIToken - the API token to query the Instana REST API (highly recommended you use a token with limited and read-only access)
3. fqdn - the FQDN of the host you want to view in Instana

The rest of this document will explain how to use this code as an IBM Cloud Function:

### Create an IBM Cloud Function using the UI
1. Login to `https://cloud.ibm.com/functions/actions` and create a new action by clicking "Create"
2. Create an entity of type "Action"
<img width="423" alt="image" src="https://user-images.githubusercontent.com/7903045/136178592-32513272-6f7e-4647-9650-10324e2802d6.png">

3. Create an action with the Python runtime and give it whatever name you want.
<img width="675" alt="image" src="https://user-images.githubusercontent.com/7903045/136178768-8359f838-587d-4246-a392-ad22851b5245.png">

4. Paste the content of the file (`redirectInstana.py`) into the online editor and save the file.
<img width="800" alt="image" src="https://user-images.githubusercontent.com/7903045/136179120-07ff36e8-6ab0-4bbb-83d4-3e200170b762.png">

5. In the "Parameters" tab, add the `instanaURL` and `instanaAPIToken` values and save. 
<img width="800" alt="image" src="https://user-images.githubusercontent.com/7903045/136179427-1188e911-b8df-414c-8060-e27190350d7a.png">

6. In the "Endpoints" tab, click the "Enable as Web Action" checkbox and save. Note/record the value of the public HTTP endpoint
![image](https://user-images.githubusercontent.com/7903045/136180119-cda6e737-24f3-4e0b-96bd-99ba316e0c4b.png)

At this point you can test your function by running the command line instruction:
```bash
curl https://<thePublicFunctionEndpoint>.json?fqdn=<Hostname.domain>
```
and getting, as a result something like this:

```bash
{
  "headers": {
    "location": "https://<instanaServer>/#/physical/dashboard?snapshotId=<snapshotId>"
  },
  "statusCode": 302
}%

```

> Note that the suffix `.json` was added to the function to display the HTTP response in your CLI window. This is not necessary in a browser.

If you enter the function in your browser (with or without the `.json` suffix), you will be redirected to the same location.

Returning to the Grafana dashboard, you can now create a drill down link which will call the function in a new browser tab and open the Instana dashboard on the host.

<img width="744" alt="image" src="https://user-images.githubusercontent.com/7903045/136182054-dcf5ed57-4fd4-4923-a9aa-56ca14960a72.png">


