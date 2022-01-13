<?php

namespace OCA\RDS\Commands;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use \OCP\IConfig;
use \OCA\RDS\Service\RDSService;


class SetUrl extends Command
{

    private $config;
    private $appName;
    private $rdsService;

    public function __construct(IConfig $config, $appName, RDSService $rdsService)
    {
        parent::__construct();
        $this->config = $config;
        $this->appName = $appName;
        $this->rdsService = $rdsService;
    }


    protected function configure()
    {
        $this
            ->setName('rds:set-url')
            ->setDescription('Sets the iframe url within RDS app.')
            ->addArgument(
                'url',
                InputArgument::REQUIRED,
                'The url for the RDS app - will be shown as iframe inside of RDS app.'
            );
    }

    /**
     * @param InputInterface $input
     * @param OutputInterface $output
     * @return int|void
     * @throws \OCP\AppFramework\Db\MultipleObjectsReturnedException
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $url = $input->getArgument('url');
        $this->config->setAppValue($this->appName, $this->rdsService->getUrlService()->getCloudUrlKey(), $url);
    }
}
