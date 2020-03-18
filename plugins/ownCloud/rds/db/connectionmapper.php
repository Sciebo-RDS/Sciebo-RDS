<?php
namespace OCA\RDS\Db;

use OCA\RDS\Db\Connection;

class ConnectionMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/project';

    public function __construct() {

    }

    public function insert( $userId ) {
        # TODO:  create a new connection in RDS and return it
        return [];
    }

    public function update( $conn ) {
        # TODO:  update a new connection in RDS and return it
        return [];
    }

    public function find( $id, $userId ) {
        # TODO:  add here the request to get specific connection for id
        return [];
    }

    public function findAll( $userId ) {
        # TODO:  add here the request to get all connections for userid
        return [];
    }

}