<?php
/**
 * @author Benedikt Kulmann <bkulmann@owncloud.com>
 *
 * @copyright Copyright (c) 2020, ownCloud GmbH
 * @license AGPL-3.0
 *
 * This code is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License, version 3,
 * as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License, version 3,
 * along with this program.  If not, see <http://www.gnu.org/licenses/>
 *
 */

namespace OCA\Web\Controller;

use OC\AppFramework\Http;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\JSONResponse;
use OCP\ILogger;
use OCP\IRequest;

/**
 * Class ConfigController
 *
 * @package OCA\Web\Controller
 */
class ConfigController extends Controller {

    /**
     * @var ILogger
     */
    private $logger;

    /**
     * ConfigController constructor.
     *
     * @param string $appName
     * @param IRequest $request
     * @param ILogger $logger
     */
    public function __construct(string $appName, IRequest $request, ILogger $logger) {
        parent::__construct($appName, $request);
        $this->logger = $logger;
    }

    /**
     * Loads the config json file for ownCloud Web
     *
	 * @PublicPage
	 * @NoCSRFRequired
     *
     * @return JSONResponse
     */
    public function getConfig(): JSONResponse {
        try {
            $configFile = \OC::$SERVERROOT . '/config/config.json';
            $configContent = \file_get_contents($configFile);
            $configAssoc = \json_decode($configContent, true);
            $response = new JSONResponse($configAssoc);
			$response->addHeader('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate');
			$response->addHeader('Pragma', 'no-cache');
			$response->addHeader('Expires', 'Wed, 11 Jan 1984 05:00:00 GMT');
			$response->addHeader('X-Frame-Options', 'DENY');
			return $response;
        } catch(\Exception $e) {
            $this->logger->logException($e, ['app' => 'web']);
            return new JSONResponse(["message" => $e->getMessage()], Http::STATUS_NOT_FOUND);
        }
    }
}
