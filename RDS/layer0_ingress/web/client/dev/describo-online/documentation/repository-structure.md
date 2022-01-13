# Repository Structure

- [Repository Structure](#repository-structure)
  - [UI structure](#ui-structure)
  - [API structure](#api-structure)
  - [configuration](#configuration)

This repo contains both the UI and API code. See the [README](../README.md) for how to run it.

## UI structure

-   The main entry point is `src/main.js`
-   The routes and store configuration are in `src/routes` and `src/store` respectively.
-   All components are in `src/components`.
-   TailwindCSS is used in this app. Please try to use tailwind as much as possible and if you do need to create custom css then scope it to the component. No global CSS unless absolutely necessary!!

## API structure

-   The main entry point is `src/index.js`
-   `src/common` contains things like loggers and type definitions
-   `src/lib` has methods and unit tests for managing entites and such
-   `src/middleware` has route middlewares
-   `src/models` contains the sequelize database models
-   `src/routes` contains the route handlers and e2e tests
-   `src/routes/index` is where route handlers are imported and wired up

## configuration

The configuration folder contains an example config file and is where docker expects to find a
development configuration which will be mounted into the right place in the running container.
