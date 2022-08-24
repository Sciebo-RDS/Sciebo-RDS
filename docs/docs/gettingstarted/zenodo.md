# Set up Zenodo

First, you have to create an separate applications especially for sciebo RDS, so first, go to the testing instance of [sandbox.zenodo.org](https://sandbox.zenodo.org/account/settings/applications/clients/new/).

If you have an account already there, you should open the settings page and redirect the browser to "Applications". There, you have to create a new application, set a unique name, a description, a website url to something useful.
The most important option is the redirect url: There you have to enter the domain you want to use for sciebo RDS. It has to have the protocol: most times `https://your-rds.institution.org`. Also you have to use the `Confidential` client type.

Now save your application. At the top of the page, you will find the `client ID` and `client secret`. Save this informations, because this will be needed on the next step.
