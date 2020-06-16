<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Project extends Entity implements JsonSerializable {

    protected $projectId;
    protected $metadata;

    public function jsonSerialize() {
        return [
            'projectId'=>$this->projectId,
            'metadata' => $this->metadata,
        ];
    }
}