# GrafanaRedirectInstana
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

![image](https://user-images.githubusercontent.com/7903045/136161610-1c9880a4-43f5-42ec-8c30-15db8c3fb819.png)

What we would like to do now is add a link in the format of `https://<instanaHostURL>/#/physical/dashboard?snapshotId=<snapshotId>`

But as you can see, `snapshotId` is not one of the available fields:

<img width="791" alt="image" src="https://user-images.githubusercontent.com/7903045/136162134-b16b6348-a707-40ed-90cc-bb3a08103ef7.png">

The solution is to create a helper function which will recieve the `series name` (in the case of hosts this is the FQDN), translate that to the most recent snapshotId and redirect the browser to the Instana server.

The code shared in this repository does this.

## The solution


