<?php

namespace OCA\RDS\Db;

use \OCA\RDS\Db\Metadata;
use \OCA\RDS\Service\NotFoundException;
use \OCA\RDS\Service\UrlService;

class MetadataMapper
{
  private $urlService;

  public function __construct(UrlService $urlService)
  {
    $this->urlService = $urlService;
  }

  public function update($metadata)
  {
    $curl = curl_init($this->urlService->getMetadataURL() . '/user/' . $metadata->getUserId() . '/research/' . $metadata->getResearchIndex());
    $options = [CURLOPT_RETURNTRANSFER => true];
    curl_setopt_array($curl, $options);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($metadata->getMetadata()));
    curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'PATCH');
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
    // Set the content type to application/json
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));

    $response = json_decode(curl_exec($curl));
    $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);

    if ($httpcode >= 300) {
      return NULL;
    }

    return true;
  }

  public function find($userId, $researchIndex, $port)
  {
    $metadatas = $this->findAll($userId, $researchIndex);

    foreach ($metadatas as $md) {
      if ($md->port == $port) {
        return $md;
      }
    }

    throw new NotFoundException('No metadata for ' . $port . ' found.');
  }

  public function jsonschema()
  {
    return json_encode([
      "kernelversion" => "custom",
      "schema" => '{
                "additionalProperties": false,
                "description": "Describe information needed for deposit module.",
                "id": "http://zenodo.org/schemas/deposits/records/legacyjson.json",
                "properties": {
                  "upload_type": {
                      "additionalProperties": false,
                      "default": "publication",
                      "description": "Record upload type.",
                      "enum": [
                          "publication",
                          "poster",
                          "presentation",
                          "dataset",
                          "image",
                          "video",
                          "software",
                          "lesson",
                          "other"
                        ],  
                      "type": "string"
                  },
                  "publication_type": {
                      "additionalProperties": false,
                      "description": "Publication type for zenodo only.",
                      "default": "other",
                      "enum": [
                          "book",
                          "section",
                          "conferencepaper",
                          "article",
                          "patent",
                          "preprint",
                          "report",
                          "deliverable",
                          "milestone",
                          "proposal",
                          "softwaredocumentation",
                          "thesis",
                          "technicalnote",
                          "workingpaper",
                          "datamanagementplan",
                          "annotationcollection",
                          "taxonomictreatment",
                          "other"
                        ],
                      "type": "string"
                  },
                  "image_type": {
                      "additionalProperties": false,
                      "default": "other",
                      "description": "Image type.",
                      "enum": [
                          "figure",
                          "plot",
                          "drawing",
                          "diagram",
                          "photo",
                          "other"
                        ],
                        "type": "string"
                  },
                  "publication_date": {
                      "description": "Format: YYYY-MM-DD. In case your upload was already published elsewhere, please use the date of first publication.",
                      "type": "string"
                  },
                  "title": {
                      "description": "Record title.",
                      "type": "string"
                  },
                  "creators": {
                      "description": "Creators of record in order of importance.",
                      "items": {
                        "additionalProperties": false,
                        "properties": {
                          "affiliation": {
                            "description": "Affiliation for the purpose of this specific record.",
                            "type": "string"
                          },
                          "gnd": {
                            "description": "Gemeinsame Normdatei identifier for creator.",
                            "type": "string"
                          },
                          "name": {
                            "description": "Full name of person or organisation. Personal name format: family, given.",
                            "type": "string"
                          },
                          "orcid": {
                            "description": "ORCID identifier for creator.",
                            "type": "string"
                          }
                        },
                        "type": "object"
                      },
                      "type": "array"
                  },
                  "description": {
                      "description": "Description/abstract for record.",
                      "type": "string"
                  },
                  "access_right": {
                      "default": "open",
                      "description": "Access right for record.",
                      "enum": [
                        "open",
                        "embargoed",
                        "restricted",
                        "closed"
                      ],
                      "type": "string"
                  },
                  "osf_category": {
                    "enum": [
                      "analysis",
                      "communication",
                      "data",
                      "hypothesis",
                      "instrumentation",
                      "methods and measures",
                      "procedure",
                      "project",
                      "software",
                      "other"
                    ],
                    "default": "other",
                    "description": "Category only for OSF",
                    "type": "string"
                  },
                  "license": {
                      "description": "License for embargoed/open access content.",
                      "title": "License",
                      "type": "string",
                      "default": "CC-BY-4.0"
                  },
                  "embargo_date": {
                      "description": "Format: YYYY-MM-DD. The date your upload will be made publicly available in case it is under an embargo period from your publisher.",
                      "title": "Embargo Date",
                      "type": "string"
                  },
                  "access_conditions": {
                    "description": "Conditions under which access is given if record is restricted.",
                    "title": "Access conditions",
                    "type": "string"
                  }
                },
                "required": ["upload_type","publication_date","title","creators","description","access_right"],
                "title": "Zenodo Legacy Deposit Schema v1.0.0",
                "type": "object"
              }'
    ]);

    $url = $this->urlService->getMetadataURL() . '/jsonschema';

    $curl = curl_init();
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
    $result = curl_exec($curl);
    $response = json_decode($result, true);
    $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);

    if ($httpcode >= 300) {
      return NULL;
    }

    return $result;
  }

  public function findAll($userId, $researchIndex)
  {
    $url = $this->urlService->getMetadataURL() . '/user/' . $userId . '/research/' . $researchIndex;

    $curl = curl_init();
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
    $result = curl_exec($curl);
    $response = json_decode($result, true);
    $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);

    if ($httpcode >= 300) {
      return NULL;
    }

    $result = [];

    foreach ($response['list'] as $rdsMetadata) {
      $metadata = new Metadata();

      $metadata->setUserId($userId);
      $metadata->setResearchIndex($researchIndex);
      $metadata->setPort($rdsMetadata['port']);
      $metadata->setMetadata($rdsMetadata['metadata']);

      $result[] = $metadata;
    }

    return $result;
  }
}
