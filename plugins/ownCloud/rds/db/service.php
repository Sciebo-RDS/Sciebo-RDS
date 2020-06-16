<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Service extends Entity implements JsonSerializable {

    protected $servicename;
    protected $authorizeUrl;
    protected $state;

    public function jsonSerialize() {
        return [
            'servicename' => $this->servicename,
            'authorizeUrl' => $this->authorizeUrl,
            'state' => $this->state,
        ];
    }
}
