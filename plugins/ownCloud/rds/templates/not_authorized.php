<?php
style('rds', array('style'));
script('rds', array('handlebars', 'CustomHelpers'));

script('rds', array('Services', 'FirstWizard'));

?>


<div class="section" id="rds">
  <div class="error_message">
    <?php
    if (isset($_["error"])) {
      p($l->t('oauth workflow was not successful finished.'));
    }
    ?>
  </div>
  <div class="welcome">
    <p>
      <?php p($l->t('Welcome. To use this app, you need to authenticate
      services to perform actions with RDS on files in the services. Please
      follow this steps.')); ?>
    </p>
  </div>
  <div class="service" id="rdsOwncloud">
    <p>
      <?php p($l->t('Step 1: Authorize RDS to authenticate against ownCloud.')); ?>
    </p>
    <button class="button" id="activateOwncloud" data-servicename="Owncloud" disabled>
      <?php p($l->t('Authorize ownCloud.')); ?>
    </button>
  </div>
  <div class="service" id="rdsZenodo">
    <p>
      <?php p($l->t('Step 2: Authorize RDS to authenticate against Zenodo.')); ?>
    </p>
    <button class="button" id="activateZenodo" data-servicename="Zenodo" disabled>
      <?php p($l->t('Authorize Zenodo.')); ?>
    </button>
  </div>
  <div class="service" id="reload">
    <p>
      <?php p($l->t('Step 3: Create a research in RDS and configure it.'));
      ?>
    </p>
    <button class="button" id="activateResearch" disabled>
      <?php p($l->t('Create a research in RDS.')); ?>
    </button>
  </div>
</div>