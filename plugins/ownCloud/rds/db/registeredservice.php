<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class RegisteredService extends Entity implements JsonSerializable {
    protected $servicename;
    protected $userId;
    protected $serviceProjects;
    protected $accessToken;
    protected $type;

    public function jsonSerialize() {
        return [
            'servicename' => $this->servicename,
            'userId' => $this->userId,
            'accessToken' => $this->accessToken,
            'serviceProjects' => $this->serviceProjects,
            'type' => $this->type,
        ];
    }
}