<?php
$rdsURL = "http://sciebords-dev.uni-muenster.de/token-service";
function getRegisteredServicesForUser()
{
    global $rdsURL;
    $curl = curl_init($rdsURL . "/user/" . $_['user_id'] . "/service");
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

    $response = json_decode(curl_exec($curl));
    $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);

    if($httpcode >= 300) {
        return [];
    }

    return $response;
}
$logged_in = false;
$services = getRegisteredServicesForUser();
foreach ($services as $service) {
    if ("Owncloud" == $service) {
        $logged_in = true;
        break;
    }
}
/** @var \OCA\OAuth2\Db\Client $client */
?>


<div class="section" id="oauth2">
    <h2 class="app-name"><?php p($l->t('Sciebo RDS')); ?></h2>

    <?php /*$logged_in = false;
    if (!empty($_['clients'])) {
        foreach ($_['clients'] as $client) {
            if ($client->getName() == "Sciebo RDS") {
                $logged_in = true;
            }
        }
    }*/

    if ($logged_in) {
    ?>

        <?php p($l->t('Which services do you want to use?')); ?>
        <p>
            <select id="svc-selector">
                <!-- JS will generate the options automatically and add them here -->
            </select>
            <button id="svc-button" class="button" disabled><?php p($l->t('Please select a service.')); ?></button>
        </p>
</div>

<div class="section" id="services" style="display: none;">
    <table id="serviceStable" data-preview-x="32" data-preview-y="32">
        <thead>
            <tr>
                <th id="servicename"><?php p($l->t("Servicename")); ?></th>
                <th id="actions"><?php p($l->t("Actions")); ?></th>
            </tr>
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
        script('rds', 'services');
    } else {
        script('rds', 'authorizeRDS');
        p($l->t('Sciebo RDS is not authorized yet.'));
?><br>
    <button id="openAuthorizeOwncloud" class="button"><?php p($l->t('Authorize Sciebo RDS now.')); ?></button>
<?php
    } ?>
</div>