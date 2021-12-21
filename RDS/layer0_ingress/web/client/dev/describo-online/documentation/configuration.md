# Describo configuration

Describo is driven by a configuration file that is loaded by the api at startup. The UI also loads
the configuration by doing a GET to `api:/configuration` when it initialises.

The configuration is a JSON object with two top level keys: `ui` and `api`. The API will send the UI
the ui configuration when the UI does a GET for it.

## UI Configuration

The UI configuration can define anything the UI needs to operate. Currently, that includes things like
the site name and log to show, max session lifetime (in seconds) and maximum number of entities to allow
saving a template.

More importantly, there is a `services` key which defines information that UI components need to operate.
These names can be anything that make sense. There is no defined structure.

## API configuration

Like the UI configuration, this is anything the API needs to operate.

Currently, the only option is the `applications` key which defines an array of external applications that
are allowed to create sessions in describo. Each must have a name, a secret and optionally, an endpoint to which
describo can POST back the crate on save.
