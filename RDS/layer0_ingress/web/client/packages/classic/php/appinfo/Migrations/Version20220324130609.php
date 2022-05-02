<?php

namespace OCA\rds\Migrations;

use OCP\Migration\ISimpleMigration;
use OCP\Migration\IOutput;

use \OCA\RDS\Service\RDSService;

/**
 * Auto-generated migration step: Please modify to your needs!
 */
class Version20220324130609 implements ISimpleMigration
{

    /**
     * @param IOutput $out
     */
    public function run(IOutput $out)
    {
        $server = \OC::$server;

        $rdsService = $server->query(RDSService::class);
        $urlService = $rdsService->getUrlService();

        $keys = $rdsService->getKeys();
        if (($urlService->getURL()  == null) || ($rdsService->getOauthValue() == null)  || ($keys[0] == null || $keys[1] == null)) {
            $out->info("Reset values for sciebo RDS, because something is missing or has a wrong value.");
            $rdsService->execute_reset();
        } else {
            $out->info("All values are set for sciebo RDS.");
        }
    }
}
