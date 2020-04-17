<h1><?php p($l->t('Project')); ?> {{research.researchIndex}}</h1>

<div id="wrapper-services">
  {{#each services}}
  <hr />
  <div id="selector-available-services">
    <b>{{ servicename }}:</b>
    <div id="radiobuttons-list">
      {{#each serviceProjects}}
      <label>
        {{#if title}}
          <input
            type="radio"
            name="radiobutton-{{ servicename }}"
            id="radiobutton-{{ title }}"
            value="{{ title }}"
          />
          {{ title }}
        {{else}}
        <input
          type="radio"
          name="radiobutton-{{ servicename }}"
          id="radiobutton- {{prereserve_doi.doi}}"
          value=" {{prereserve_doi.doi}}"
        />
          <?php p($l->t('Project DOI')); ?>: {{prereserve_doi.doi}} (<?php p($l->t('No title found.')); ?>)
        {{/if}}
      </label>
      {{else}}
      <?php p($l->t('No projects found.')); ?>
      {{/each}}
    </div>
    <div id="service-configuration">
      <div id="service-configuration-transfergoing">
        <?php p($l->t('For which transfer, do you want to use this service?')); ?>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-going"
            id="checkbox-{{ servicename }}-ingoing"
            value="portIn"
          />
          <?php p($l->t('Ingoing')); ?>
        </label>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-going"
            id="checkbox-{{ servicename }}-outgoing"
            value="portOut"
          />
          <?php p($l->t('Outgoing')); ?>
        </label>
      </div>
      <div id="service-configuration-status">
      <?php p($l->t('For which storage, do you want to use this service?')); ?>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-property"
            id="checkbox-{{ servicename }}-filestorage"
            value="fileStorage"
          />
          <?php p($l->t('File Storage')); ?>
        </label>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-property"
            id="checkbox-{{ servicename }}-metadata"
            value="metadata"
          />
          <?php p($l->t('Metadata Storage')); ?>
        </label>
      </div>
    </div>
  </div>
  {{/each}}
</div>

<div id="wrapper-custom-buttons">
  <button id="btn-add-new-service"><?php p($l->t('Add new service')); ?></button>
  <div id="spacer"></div>
  <button id="btn-save-research"><?php p($l->t('Save')); ?></button>
  <button id="btn-save-research-and-continue"><?php p($l->t('Save & continue')); ?></button>
</div>
