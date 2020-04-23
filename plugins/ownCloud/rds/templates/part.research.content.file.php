this are the fields of files

<label>
    <input type="checkbox" id="checkbox-automatic-upload">
    <?php p($l->t('Files auto upload')); ?>
    <a href="#" id="helper-auto-upload" title="<?php p($l->t('The system will upload all files in the given folder after some time.')); ?>"><img src="core/img/actions/info.svg" /></a>
</label>
<label>
    <input type="checkbox" id="checkbox-apply-changes">
    <?php p($l->t('Apply file changes')); ?>
    <a href="#" id="helper-apply-changes" title="<?php p($l->t('Otherwise deletions or file changes are not synchronized to the given services.')); ?>"><img src="core/img/actions/info.svg" /></a>
</label>

<div id="wrapper-custom-buttons">
  <div id="spacer"></div>
  <button id="btn-sync-files"><?php p($l->t('Synchronize files')); ?></button>
  <button id="btn-finish-research"><?php p($l->t('Finish research')); ?></button>
</div>