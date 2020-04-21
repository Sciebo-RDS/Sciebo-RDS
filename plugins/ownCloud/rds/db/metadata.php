<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Metadata extends Entity implements JsonSerializable {

    protected $userId;
    protected $researchIndex;
    protected $port;
    protected $metadata;

    public function jsonSerialize() {
        return [
            'userId'=>$this->userId,
            'researchIndex' => $this->researchIndex,
            'port' => $this->port,
            'metadata' => $this->metadata
        ];
    }
}