
<?php p($l->t('Here you can finalize your research project or synchronize all files with your defined services.')); ?>

<div class="wrapper-auto-upload">
    <label>
        <input type="checkbox" id="checkbox-automatic-upload">
        <?php p($l->t('Files auto upload')); ?>
        <a target="_blank" rel="noreferrer" class="icon-info"  href="#"
	   title="<?php p($l->t('The system will upload all files in the given folder after some time.')); ?>"></a>
    </label>
</div>
<div class="wrapper-apply-changes">
    <label>
        <input type="checkbox" id="checkbox-apply-changes">
        <?php p($l->t('Apply file changes')); ?>
        <a target="_blank" rel="noreferrer" class="icon-info"  href="#"
        title="<?php p($l->t('Otherwise deletions or file changes are not synchronized to the given services.')); ?>"></a>
    </label>
</div>

<div class="wrapper-custom-buttons">
  <div class="spacer"></div>
  <button id="btn-save-files"><?php p($l->t('Save')); ?></button>
  <button id="btn-sync-files"><?php p($l->t('Synchronize files')); ?></button>
  <button id="btn-finish-research"><?php p($l->t('Finish research')); ?></button>
</div>