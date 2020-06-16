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

    function __construct() {
        $this->portIn = [];
        $this->portOut = [];
    }
   
    public function addImport( $port ) {
        $this->portIn[] = $port;
    }
    
    public function addExport( $port ) {
        $this->portOut[] = $port;
    }

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