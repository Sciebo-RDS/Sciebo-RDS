<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Research extends Entity implements JsonSerializable {

    protected $userId;
    protected $researchIndex;
    protected $researchId;
    protected $status;
    protected $portsIn;
    protected $portsOut;

    function __construct() {
        $this->portsIn = [];
        $this->portsOut = [];
    }

    public function addImport( $port ) {
        $this->portsIn[] = $port;
    }

    public function addExport( $port ) {
        $this->portsOut[] = $port;
    }

    public function jsonSerialize() {
        return [
            'userId' => $this->userId,
            'researchIndex' => $this->researchIndex,
            'researchId' => $this->researchId,
            'status' => $this->status,
            'portIn' => $this->portsIn,
            'portOut' => $this->portsOut
        ];
    }
}