<h1><?php p($l->t('Project')); ?> {{research.researchIndex}}</h1>

<div id="wrapper-services">
  {{#each services}}
  <hr />
  <div id="selector-available-services">
    <b>{{ servicename }}:</b>
    {{#if type.fileStorage}}
    <div id="fileStorage-wrapper">
      <button id="btn-open-folderpicker">Select folder</button>
    </div>
    {{/if}}
    {{#if type.fileStorage}}
    <div id="radiobuttons-list">
      {{#each serviceProjects}}
      <label>
          <input
            type="radio"
            name="radiobutton-{{ ../servicename }}"
            id="{{ ../servicename }}-{{prereserve_doi.recid}}"
            value="{{prereserve_doi.recid}}"
            {{ checked }}
          />
        {{#if title}}
          {{ title }}
        {{else}}
          <?php p($l->t('Project DOI')); ?>: {{prereserve_doi.doi}} (<?php p($l->t('No title found.')); ?>)
        {{/if}}
      </label>
      {{else}}
      <?php p($l->t('No projects found.')); ?>
      {{/each}}
    </div>
    {{/if}}
    <div id="service-configuration">
      <div id="service-configuration-transfergoing">
        <?php p($l->t('For which transfer, do you want to use this service?')); ?> 
        <a target="_blank" rel="noreferrer" class="icon-info"  href="#" title="<?php p($l->t('Informations about ingoing and outgoing traffic.')); ?>"></a>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-going"
            id="checkbox-{{ servicename }}-ingoing"
            value="portIn"
            {{ importChecked }}
          />
          <?php p($l->t('Ingoing')); ?>
        </label>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-going"
            id="checkbox-{{ servicename }}-outgoing"
            value="portOut"
            {{ exportChecked }}
          />
          <?php p($l->t('Outgoing')); ?>
        </label>
      </div>
      <div id="service-configuration-status">
      <?php p($l->t('For which storage, do you want to use this service?')); ?>
      <a target="_blank" rel="noreferrer" class="icon-info"  href="#" title="<?php p($l->t('Informations about storage for metadata and fileStorage.')); ?>"></a>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-property"
            id="checkbox-{{ servicename }}-filestorage"
            value="fileStorage"
            {{ fileStorageChecked }}
          />
          <?php p($l->t('File Storage')); ?>
        </label>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-property"
            id="checkbox-{{ servicename }}-metadata"
            value="metadata"
            {{ metadataChecked }}
          />
          <?php p($l->t('Metadata Storage')); ?>
        </label>
      </div>
    </div>
  </div>
  {{/each}}
</div>

<div id="wrapper-custom-buttons">
  <div id="spacer"></div>
  <button id="btn-save-research"><?php p($l->t('Save')); ?></button>
  <button id="btn-save-research-and-continue"><?php p($l->t('Save & continue')); ?></button>
</div>
