<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Research extends Entity implements JsonSerializable {

    protected $userId;
    protected $researchIndex;
    protected $researchId;
    protected $status;
    protected $portIn;
    protected $portOut;

    public function jsonSerialize() {
        return [
            'userId' => $this->userId,
            'researchIndex' => $this->researchIndex,
            'researchId' => $this->researchId,
            'status' => $this->status,
            'portIn' => $this->portIn,
            'portOut' => $this->portOut
        ];
    }
}