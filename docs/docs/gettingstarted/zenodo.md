# Setting up Zenodo

1. [Create a Zenodo test application](](https://sandbox.zenodo.org/account/settings/applications/clients/new/)) to get API access for your sciebo RDS instance.

If you already have an account there, open the settings page and redirect the browser to "Applications". Create a new application, set a unique name, a description, a website url to something useful.
The most important field is the `redirect url`, which has to match the domain of your sciebo RDS instance (e.g. `your-rds.institution.org`).    
You also have to use the `Confidential` client type.

2. The first step will give you a Zenodo `Client ID` and `Client secret`.   

Place it in your `values.yaml` as shown in the next section, [Configuting Kubernetes](./kubernetes.md).