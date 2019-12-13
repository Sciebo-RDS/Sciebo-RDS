<?php

/** @var \OCA\OAuth2\Db\Client $client */
script('rds', 'services');
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

        <?php p($l->t('Which services do you want to use?')); ?>
        <select id="svc-selector">
        </select>
        <button id="svc-button" class="button" disabled><?php p($l->t('Please select a service.')); ?></button>
</div>

<div class="section" id="services">
    <table id="serviceStable" data-preview-x="32" data-preview-y="32">
        <thead>
            <th id="servicename"><?php p($l->t("Servicename")); ?></th>
            <th id="actions"><?php p($l->t("Actions")); ?></th>
        </thead>
        <tbody id="serviceList">
        </tbody>
    </table>
</div>


<div class="section" id="rds">
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