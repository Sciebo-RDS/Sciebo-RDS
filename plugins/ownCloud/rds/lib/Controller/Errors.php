<?php

namespace OCA\RDS\Controller;

use Closure;

use OCP\AppFramework\Http;
use OCP\AppFramework\Http\JSONResponse;
use \OCA\RDS\Service\NotFoundException;


trait Errors {

    protected function handleNotFound (Closure $callback) {
        try {
            return new JSONResponse($callback());
        } catch(NotFoundException $e) {
            $message = ['message' => $e->getMessage()];
            return new JSONResponse($message, Http::STATUS_NOT_FOUND);
        }
    }

}