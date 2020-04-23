this are the fields of files

<div id="wrapper-auto-upload">
    <label>
        <input type="checkbox" id="checkbox-automatic-upload">
        <?php p($l->t('Files auto upload')); ?>
        <a target="_blank" rel="noreferrer" class="icon-info"  href="#"
	   title="<?php p($l->t('The system will upload all files in the given folder after some time.')); ?>"></a>
    </label>
</div>
<div id="wrapper-apply-changes">
    <label>
        <input type="checkbox" id="checkbox-apply-changes">
        <?php p($l->t('Apply file changes')); ?>
        <a target="_blank" rel="noreferrer" class="icon-info"  href="#"
        title="<?php p($l->t('Otherwise deletions or file changes are not synchronized to the given services.')); ?>"></a>
    </label>
</div>

<div id="wrapper-custom-buttons">
  <div id="spacer"></div>
  <button id="btn-sync-files"><?php p($l->t('Synchronize files')); ?></button>
  <button id="btn-finish-research"><?php p($l->t('Finish research')); ?></button>
</div>