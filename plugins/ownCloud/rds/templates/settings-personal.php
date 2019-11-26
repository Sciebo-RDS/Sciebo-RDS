<?php

/**
 * @author Project Seminar "sciebo@Learnweb" of the University of Muenster
 * @copyright Copyright (c) 2017, University of Muenster
 * @license AGPL-3.0
 *
 * This code is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License, version 3,
 * as published by the Free Software logged_in$logged_ination.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License, version 3,
 * along with this program.  If not, see <http://www.gnu.org/licenses/>
 */

/** @var \OCA\OAuth2\Db\Client $client */
?>

<div class="section" id="oauth2">
    <h2 class="app-name"><?php p($l->t('Sciebo RDS')); ?></h2>

    <?php $logged_in = false;
    if (!empty($_['clients'])) {
        foreach ($_['clients'] as $client) {
            if ($client->getName() == "Sciebo RDS") {
                $logged_in = true;
            }
        }
    }

    if ($logged_in) {
        ?>


        Which services do you want to use?
        <select id="svc-selector">
            <option value="zenodo">Zenodo</option>
        </select>
        <button id="svc-button" class="button" disabled><?php p($l->t('Please select a service.')); ?></button>
</div>

<div class="section">
    <?php p($l->t('Do you want to revoke the access for Sciebo RDS?')); ?>
    <form id="form-inline" class="delete" data-confirm="<?php p($l->t('Are you sure you want to delete this item?')); ?>" action="<?php p($_['urlGenerator']->linkToRoute('oauth2.settings.revokeAuthorization', ['id' => $client->getId()])); ?>" method="post">
        <input type="hidden" name="requesttoken" value="<?php p($_['requesttoken']) ?>" />
        <input type="submit" class="button icon-delete" value="">
    </form>
<?php
} else {
    p($l->t('Sciebo RDS is not authorized yet.'));
    ?><br>
    <button onclick="window.location.href=OC.generateUrl('/apps/oauth2/authorize')+'?response_type=code&client_id=S4MQ9MjTqb2sV47noTsQJ6REijG0u0LkScWJA2VG3LHkq7ue5t3CQPlu4ypX7RkS&redirect_uri=http:\/\/sciebords-dev.uni-muenster.de/oauth2/redirect" class="button"><?php p($l->t('Authorize Sciebo RDS now.')); ?></button>
<?php
} ?>
</div>