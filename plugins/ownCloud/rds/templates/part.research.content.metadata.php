
<?php

style( 'rds', array('brutusin-json-forms.min') );
script( 'rds', array("brutusin-json-forms.min") );

?>

<!-- Load the metadata editor -->
<div id="metadata-jsonschema-editor"></div>

<div id="wrapper-custom-buttons">
  <div id="spacer"></div>
  <button id="btn-save-metadata"><?php p($l->t('Save')); ?></button>
  <button id="btn-save-metadata-and-continue"><?php p($l->t('Save & continue')); ?></button>
  <button id="btn-skip">Skip</button>
</div>
