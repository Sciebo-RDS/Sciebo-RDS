# Testing code

- [Testing code](#testing-code)
  - [Data generation](#data-generation)
  - [Testing](#testing)
  - [Cleaning up](#cleaning-up)
  - [Results](#results)
- [Testing process](#testing-process)

The code in this folder is for testing DB operations on a database with content. There are two stages: data generation and testing.

## Data generation

To generate fake data in the DB do:

```
./run gendata
```

You can vary the content generated by editing the variables in `docker-compose-datagen.yml`:

-   N_COLLECTIONS: the number of collections to create
-   N_ENTITIES_PER_COLLECTION: the number of entities per collection
-   N_PROPERTIES_PER_ENTITY: the number of properties per entity - these will be a random mix of simple and link properties.

Once the script has run (and it can take a while depending on how you want to generate) hit `ctrl C` to stop the process but don't run `docker-compose stop`.

## Testing

After you've generated some data you can then run the tests which are in the file `test-inserts.spec.js`. This is a series of tests to time DB operations as the size of the DB grows.

```
./run test
```

## Cleaning up

Run the stop script to remove the containers and cleanup: `./stop`

## Results

Results are in the spreadsheet: `performance-testing.xlsx`

# Testing process

Basically:

-   edit the data gen variables in `docker-compose-datagen.yml`
-   create some fake data: `./run gendata`
-   run the tests: `./run test`
-   Rinse and repeat