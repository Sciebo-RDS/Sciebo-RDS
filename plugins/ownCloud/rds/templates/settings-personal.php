<?php

function getRegisteredServicesForUser($rdsURL, $userId)
{
    $curl = curl_init($rdsURL . '/user/' . $userId . '/service');
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);

    $response = curl_exec($curl);
    $json = json_decode($response);
    $httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);

    if ($httpcode >= 300) {
        return [];
    }

    return $json->list;
}
$found = false;
$services = getRegisteredServicesForUser($_["rdsURL"], $_['user_id']);

foreach ($services as $service) {
    if ($service->servicename == 'Owncloud') {
        $found = true;
        break;
    }
}

$logged_in = false;
if (!empty($_['clients'])) {
    foreach ($_['clients'] as $client) {
        if (($client->getName() == $_["oauthname"]) and $found) {
            $logged_in = true;
            break;
        }
    }
}

/** @var \OCA\OAuth2\Db\Client $client */
?>

<div class='section' id='oauth2'>
    <h2 class='app-name'><?php p($l->t('Sciebo RDS'));
                            ?></h2>

    <?php

    if ($logged_in) {
    ?>

        <?php p($l->t('Which services do you want to use?'));
        ?>
        <p>
            <select id='svc-selector'>
                <!-- JS will generate the options automatically and add them here -->
            </select>
            <button id='svc-button' class='button' disabled><?php p($l->t('Please select a service.'));
                                                            ?></button>
        </p>
</div>

<div class='section' id='services' style='display: none;'>
    <table id='serviceStable' data-preview-x='32' data-preview-y='32' width='100%'>
        <thead>
            <tr>
                <th id='servicename'><?php p($l->t('Servicename'));
                                        ?></th>
                <th id='actions'><?php p($l->t('Actions'));
                                    ?></th>
            </tr>
        </thead>
        <tbody id='serviceList'>
        </tbody>
    </table>
</div>

<div class='section' id='rds'>
    <?php p($l->t('Do you want to revoke the access for Sciebo RDS?'));

        /* TODO: remove the Owncloud access token from token storage ( otherwise it will be revoked in the next refresh step automatically ) */
    ?>

    <button id='owncloud-button-removal' class='button icon-delete'></button>
<?php
        script('rds', 'settings-personal');
    } else {
        script('rds', 'authorizeRDS');
        p($l->t('Sciebo RDS is not authorized yet.'));
?><br>
    <button id='openAuthorizeOwncloud' class='button'><?php p($l->t('Authorize Sciebo RDS now.'));
                                                        ?></button>
<?php
    }
?>
</div>