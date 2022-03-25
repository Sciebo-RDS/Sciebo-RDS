<?php

namespace OCA\RDS\Commands;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use \OCP\IConfig;
use \OCA\RDS\Service\RDSService;


class CreateKeys extends Command
{

    private $config;
    private $appName;
    private $rdsService;

    public function __construct($AppName, IConfig $config, RDSService $rdsService)
    {
        parent::__construct();
        $this->appName = $AppName;
        $this->config = $config;
        $this->rdsService = $rdsService;
    }


    protected function configure()
    {
        $this
            ->setName('rds:create-keys')
            ->setDescription('Creates the private and public key to sign informations.');
    }

    /**
     * @param InputInterface $input
     * @param OutputInterface $output
     * @return int|void
     * @throws \OCP\AppFramework\Db\MultipleObjectsReturnedException
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $keys = $this->rdsService->createKeys();

        if ($keys[0] != null && $keys[1] != null) {
            $output->writeln("Creates keys successful.");
        } else {
            $output->writeln("Cannot create keys.");
        }
    }
}
