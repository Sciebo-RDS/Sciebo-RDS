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

    /**
    * @param OCA\RDS\Db\Port $port
    * @param string $where
    * @return NULL
    */

    private function addPort( $port, $where ) {
        if ( $where == 'import' ) {
            $portsIn[] = $port;
        } else if ( $where == 'export' ) {
            $portsOut[] = $port;
        }
    }

    public function addImport( $port ) {
        $this->addPort( $port, 'import' );
    }

    public function addExport( $port ) {
        $this->addPort( $port, 'export' );
    }

    public function jsonSerialize() {
        return [
            'userId' => $this->userId,
            'researchIndex' => $this->researchIndex,
            'researchId' => $this->researchId,
            'status' => $this->status,
            'portsIn' => $this->portsIn,
            'portsOut' => $this->portsOut
        ];
    }
}