<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Connection extends Entity implements JsonSerializable {

    protected $userId;
    protected $projectIndex;
    protected $projectId;
    protected $status;
    protected $portIn;
    protected $portOut;

    public function jsonSerialize() {
        return [
            'userId' => $this->userId,
            'projectIndex' => $this->projectIndex,
            'projectId' => $this->projectId,
            'status' => $this->status,
            'portIn' => $this->portIn,
            'portOut' => $this->portOut
        ];
    }
}