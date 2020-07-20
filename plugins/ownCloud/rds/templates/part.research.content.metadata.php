
<?php

style( 'rds', array('brutusin-json-forms.min') );
script( 'rds', array("brutusin-json-forms.min") );

?>

<?php p($l->t('Here you enter your metadata informations about your research.')); ?>

<!-- Load the metadata editor -->
<div id="metadata-jsonschema-editor"><div class="icon-loading"></div></div>

<div id="wrapper-custom-buttons">
  <div class="spacer"></div>
  <button id="btn-save-metadata"><?php p($l->t('Save')); ?></button>
  <button id="btn-save-metadata-and-continue"><?php p($l->t('Save & continue')); ?></button>
  <button id="btn-skip"><?php p($l->t('Skip')); ?></button>
</div>
