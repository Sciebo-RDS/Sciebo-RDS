<?php

namespace OCA\RDS\Controller;

use OCP\IRequest;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use \OCA\RDS\Service\UrlService;


class SettingsController extends Controller
{
    private $userId;
    private $urlService;

    use Errors;

    public function __construct($AppName, IRequest $request, $urlService, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
        $this->urlService = $urlService;
    }

    /**
     * Returns all settings
     *
     * @return string returns all settings variables in RDS.
     * 
     */
    public function index()
    {
        return new JSONResponse($this->urlService->getOverview());
    }

    /**
     * Updates the URL setting
     *
     * @param array $value
     * @return string returns all settings variables in RDS.
     *
     */
    public function update($value)
    {
        $this->urlService->setURL($value);
        return new JSONResponse($this->urlService->getOverview());
    }
}
