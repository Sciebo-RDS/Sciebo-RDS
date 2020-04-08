<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Metadata extends Entity implements JsonSerializable {

    protected $researchId;
    protected $port;
    protected $metadata;

    public function jsonSerialize() {
        return [
            'researchId' => $this->researchId,
            'port' => $this->port,
            'metadata' => $this->metadata
        ];
    }
}