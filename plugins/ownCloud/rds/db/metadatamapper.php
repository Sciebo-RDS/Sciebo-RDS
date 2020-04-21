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

            $metadata->setUserId($userId);
            $metadata->setResearchIndex( $researchIndex );
            $metadata->setMetadata( $rdsMetadata['metadata'] );
            $metadata->setPort( $rdsMetadata['port'] );

            $result[] = $metadata;
        }

        return $result;
    }

}