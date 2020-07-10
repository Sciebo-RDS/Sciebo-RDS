<?php

/** @var \OCP\IL10N $l */
/** @var array $_ */
script('rds', 'settings-admin');
?>

<div id="rdsSettings" class="section">
    <h2 class="app-name has-documentation"><?php p($l->t('Research Data Services')); ?></h2>

    <a target="_blank" rel="noreferrer" class="icon-info" title="<?php p($l->t('Open documentation')); ?>" href="https://www.research-data-services.org/doc/getting-started/config/"></a>

    <p>
        <form id="rds-settings">
            <input type="text" name="cloudURL" id="cloud_url" class="text" <?php if (!empty($_["cloudURL"])) { ?> value="<?php print_unescaped($_['cloudURL']); ?>" <?php } ?> placeholder="<?php p($l->t('url to rds instance')); ?>" />
            <label for="cloudURL">
                <?php p($l->t('Specify here the URL, where the ownCloud instance can find your RDS instance e.g. https://url-to-rds-in-k8s. Please leave out the trailing slash.')); ?>
            </label>
        </form>
        <button id="rds_submit" type="button" class="button"><?php p($l->t('Save')); ?></button>
    </p>
</div>