# Introduction
CITA-Cloud automations using [Robusta](https://github.com/robusta-dev/robusta)

1. set schedule to adjust system config.

More to come soon!

[See the Robusta docs on manual triggers to understand how this works](https://docs.robusta.dev/master/getting-started/manual-triggers.html)

# Usage

### run test webhook server

We use webhook sink for test.

```
python webhook_server.py 
```

### config Robusta

```
pip install -U robusta-cli --no-cache
export PATH=$HOME/.local/bin:$PATH
```

```
robusta gen-config
```
All question select No, then we will got `generated_values.yaml`.

Edit `custom_values.yaml`(set real url of webhook_sink), then merge these two file together.

```
yq ea '. as $item ireduce ({}; . * $item )' generated_values.yaml custom_values.yaml > file-merged.yaml
```

### install Robusta
```
helm repo add robusta https://robusta-charts.storage.googleapis.com && helm repo update
helm install robusta robusta/robusta -f ./file-merged.yaml --set isSmallCluster=true
```

### update Robusta

```
helm upgrade robusta robusta/robusta --values=file-merged.yaml
```
