<?php
namespace OCA\RDS\Db;

use OCA\RDS\Db\Metadata;

class MetadataMapper {
    private $rdsURL = 'https://sciebords-dev.uni-muenster.de/metadata';

    public function __construct() {

    }

    public function update( $metadata ) {
        $curl = curl_init( $this->rdsURL . '/research/' . $metadata->researchId );
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

            $newMetadata->setResearchId( $metadata->researchId );
            $newMetadata->setMetadata( $rdsMetadata['metadata'] );
            $newMetadata->setPort( $rdsMetadata['port'] );

            $result[] = $newMetadata;
        }

        return $result;
    }

    public function find( $researchId, $port ) {
        $metadatas = $this->findAll( $researchId );

        foreach ( $metadatas as $md ) {
            if ( $md->port == $port ) {
                return $md;
            }
        }

        throw new DoesNotExistException( 'No metadata for '. $port .' found.' )
    }

    public function findAll( $researchId ) {
        $url = $this->rdsURL . '/research/' . $researchId;

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

            $metadata->setResearchId( $researchId );
            $metadata->setMetadata( $rdsMetadata['metadata'] );
            $metadata->setPort( $rdsMetadata['port'] );

            $result[] = $metadata;
        }

        return $result;
    }

}