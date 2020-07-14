<?php

namespace OCA\RDS\Db;

use \OCA\RDS\Db\Project;
use \OCA\RDS\Service\UrlService;
use \OCA\RDS\Service\NotFoundException;

class ProjectsMapper
{
    private $urlService;

    public function __construct(UrlService $urlService)
    {
        $this->urlService = $urlService;
    }

    public function findAll($userId, $servicename)
    {
        $curl = curl_init($this->urlService->getPortURL() . '/user/' . $userId . '/service/' . $servicename . '/projects');
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl), true);
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        $info = curl_getinfo($curl);
        curl_close($curl);

        if ($httpcode >= 300) {
            throw new NotFoundException(json_encode([
                'http_code' => $httpcode,
                'json_error_message' => json_last_error_msg(),
                'curl_error_message' => $info
            ]));
        }

        $listOfProj = [];

        foreach ((array) $response as $element) {
            $project = new Project();
            $project->setProjectId($element['projectId']);
            $project->setMetadata($element['metadata']);

            $listOfProj[] = $project;
        }

        return $listOfProj;
    }

    public function find($userId, $servicename, $projectId)
    {
        $curl = curl_init($this->urlService->getPortURL() . '/user/' . $userId . '/service/' . $servicename . '/projects/' . $projectId);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl), true);
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        $info = curl_getinfo($curl);
        curl_close($curl);

        if ($httpcode >= 300) {
            throw new NotFoundException(json_encode([
                'http_code' => $httpcode,
                'json_error_message' => json_last_error_msg(),
                'curl_error_message' => $info
            ]));
        }

        $project = new Project();
        $project->setProjectId($response['projectId']);
        $project->setMetadata($response['metadata']);

        return $project;
    }

    public function insert($userId, $servicename)
    {
        $curl = curl_init($this->urlService->getPortURL() . '/user/' . $userId . '/service/' . $servicename . '/projects');
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'POST'];
        curl_setopt_array($curl, $options);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl));
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        $info = curl_getinfo($curl);
        curl_close($curl);

        if ($httpcode >= 300) {
            throw new NotFoundException(json_encode([
                'http_code' => $httpcode,
                'json_error_message' => json_last_error_msg(),
                'curl_error_message' => $info
            ]));
        }

        $projs = $this->findAll($userId, $servicename);
        #        $proj = end( ( array_values( $projs ) ) );
        $index = 0;
        $max = 0;
        $i = 0;
        foreach ($projs as $proj) {
            if ($proj->getProjectId() > $max) {
                $max = $proj->getProjectId();
                $index = $i;
            }

            $i++;
        }
        return $projs[$index];
    }

    public function delete($userId, $servicename, $projectId)
    {
        $curl = curl_init($this->urlService->getPortURL() . '/user/' . $userId . '/service/' . $servicename . '/projects/' . $projectId);
        $options = [CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => 'DELETE'];
        curl_setopt_array($curl, $options);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

        $response = json_decode(curl_exec($curl));
        $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);

        return $httpcode == 204;
    }
}
