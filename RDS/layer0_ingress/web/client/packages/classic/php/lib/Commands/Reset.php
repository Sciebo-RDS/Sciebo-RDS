<?php

namespace OCA\RDS\Commands;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use \OCP\IConfig;
use \OCA\RDS\Service\RDSService;


class Reset extends Command
{

    private $config;
    private $appName;
    private $rdsService;
    private $urlService;

    public function __construct($AppName, RDSService $rdsService)
    {
        parent::__construct();
        $this->appName = $AppName;
        $this->rdsService = $rdsService;
    }


    protected function configure()
    {
        $this
            ->setName('rds:reset')
            ->setDescription('Resets values in owncloud config');
    }

    /**
     * @param InputInterface $input
     * @param OutputInterface $output
     * @return int|void
     * @throws \OCP\AppFramework\Db\MultipleObjectsReturnedException
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $this->rdsService->execute_reset();
        $output->writeln("Reset executed.");
    }
}
