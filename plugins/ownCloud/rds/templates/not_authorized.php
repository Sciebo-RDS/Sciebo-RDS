<?php
style( 'rds', array( 'style' ) );
script( 'rds', array( 'handlebars' ) );

script( 'rds', array( 'Services', 'FirstWizard' ) );

?>

<div class="section" id="rds">
  <div class="service" id="owncloud">
    <p>
      <?php p( $l->t( 'Step 1: Authorize RDS to authenticate against ownCloud.'
      ) ); ?>
    </p>
    <button class="button" id="activateOwncloud">
      <?php p( $l->t( 'Authorize ownCloud.' ) ); ?>
    </button>
  </div>
  <div class="service" id="zenodo">
    <p>
      <?php p( $l->t( 'Step 2: Authorize RDS to authenticate against Zenodo.' )
      ); ?>
    </p>
    <button class="button" id="activateZenodo" disabled>
      <?php p( $l->t( 'Authorize Zenodo.' ) ); ?>
    </button>
  </div>
  <div class="service" id="reload">
    <p>
      <?php p( $l->t( 'Step 3: Create a research in RDS and configure it.' ) );
      ?>
    </p>
    <button class="button" id="activateResearch">
      <?php p( $l->t( 'Create a research in RDS.' ) ); ?>
    </button>
  </div>
</div>
