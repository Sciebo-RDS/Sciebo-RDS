<?php
namespace OCA\RDS\Db;

use \OCA\RDS\Db\Metadata;
use \OCA\RDS\Service\NotFoundException;

class MetadataMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/metadata';

    public function __construct() {

    }

    public function update( $metadata ) {
        $curl = curl_init( $this->rdsURL . '/user/' . $metadata->getUserId(). '/research/' . $metadata->getResearchIndex() );
        $options = [CURLOPT_RETURNTRANSFER => true];
        curl_setopt_array( $curl, $options );
        curl_setopt( $curl, CURLOPT_POSTFIELDS, $metadata->jsonSerialize() );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );

        $response = json_decode( curl_exec( $curl ) );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        $result = [];

        foreach ( $response['list'] as $rdsMetadata ) {
            $newMetadata = new Metadata();

            $newMetadata->setUserId( $metadata->getUserId() );
            $newMetadata->setResearchIndex( $metadata->getResearchIndex() );
            $newMetadata->setMetadata( $rdsMetadata['metadata'] );
            $newMetadata->setPort( $rdsMetadata['port'] );

            $result[] = $newMetadata;
        }

        return $result;
    }

    public function find( $userId, $researchIndex, $port ) {
        $metadatas = $this->findAll( $userId, $researchIndex );

        foreach ( $metadatas as $md ) {
            if ( $md->port == $port ) {
                return $md;
            }
        }

        throw new NotFoundException( 'No metadata for '. $port .' found.' );
    }

    public function jsonschema() {
        return [
            "kernelversion" =>"custom",
            "schema" => '{
            "$schema": "http://json-schema.org/draft-07/schema",
            "$id": "http://example.com/example.json",
            "type": "object",
            "title": "The root schema",
            "description": "The root schema comprises the entire JSON document.",
            "default": {},
            "examples": [
                {
                    "upload_type": "poster",
                    "description": "This is my first upload",
                    "creators": [
                        {
                            "name": "Doe, John",
                            "affiliation": "Zenodo"
                        }
                    ]
                }
            ],
            "required": [
                "upload_type",
                "description",
                "creators"
            ],
            "additionalProperties": true,
            "properties": {
                "upload_type": {
                    "$id": "#/properties/upload_type",
                    "type": "string",
                    "title": "The upload_type schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": "",
                    "examples": [
                        "poster"
                    ]
                },
                "description": {
                    "$id": "#/properties/description",
                    "type": "string",
                    "title": "The description schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": "",
                    "examples": [
                        "This is my first upload"
                    ]
                },
                "creators": {
                    "$id": "#/properties/creators",
                    "type": "array",
                    "title": "The creators schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": [],
                    "examples": [
                        [
                            {
                                "name": "Doe, John",
                                "affiliation": "Zenodo"
                            }
                        ]
                    ],
                    "additionalItems": true,
                    "items": {
                        "anyOf": [
                            {
                                "$id": "#/properties/creators/items/anyOf/0",
                                "type": "object",
                                "title": "The first anyOf schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "name": "Doe, John",
                                        "affiliation": "Zenodo"
                                    }
                                ],
                                "required": [
                                    "name",
                                    "affiliation"
                                ],
                                "additionalProperties": true,
                                "properties": {
                                    "name": {
                                        "$id": "#/properties/creators/items/anyOf/0/properties/name",
                                        "type": "string",
                                        "title": "The name schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "Doe, John"
                                        ]
                                    },
                                    "affiliation": {
                                        "$id": "#/properties/creators/items/anyOf/0/properties/affiliation",
                                        "type": "string",
                                        "title": "The affiliation schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "Zenodo"
                                        ]
                                    }
                                }
                            }
                        ],
                        "$id": "#/properties/creators/items"
                    }
                }
            }
        }'];

        $url = $this->rdsURL . '/jsonschema';

        $curl = curl_init();
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_URL, $url );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );
        $result = curl_exec( $curl );
        $response = json_decode( $result, true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        return $result;
    }

    public function findAll( $userId, $researchIndex ) {
        $url = $this->rdsURL . '/user/' . $userId . '/research/' . $researchIndex;

        $curl = curl_init();
        curl_setopt( $curl, CURLOPT_RETURNTRANSFER, true );
        curl_setopt( $curl, CURLOPT_URL, $url );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYPEER, false );
        curl_setopt( $curl, CURLOPT_SSL_VERIFYHOST, false );
        $result = curl_exec( $curl );
        $response = json_decode( $result, true );
        $httpcode = curl_getinfo( $curl, CURLINFO_HTTP_CODE );
        curl_close( $curl );

        if ( $httpcode >= 300 ) {
            return NULL;
        }

        $result = [];

        foreach ( $response['list'] as $rdsMetadata ) {
            $metadata = new Metadata();

            $metadata->setUserId( $userId );
            $metadata->setResearchIndex( $researchIndex );
            $metadata->setPort( $rdsMetadata['port'] );
            $metadata->setMetadata( $rdsMetadata['metadata'] );

            $result[] = $metadata;
        }

        return $result;
    }

}