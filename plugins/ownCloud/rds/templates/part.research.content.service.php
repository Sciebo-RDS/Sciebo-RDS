this are the fields for services

<div id="wrapper-services">
  {{#each services}}
  <div id="selector-available-services">
    <b>{{ servicename }}:</b>
    <div id="radiobuttons-list">
      {{#each serviceProjects}}
      <label>
        <input
          type="radio"
          name="radiobutton-{{ servicename }}"
          id="radiobutton-{{ projectname }}"
          value="{{ projectname }}"
        />
        {{ projectname }}
      </label>
      {{/each}}
    </div>
    <div id="service-configuration">
      <div id="service-configuration-transfergoing">
        For which transfer, do you want to use this service?
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-going"
            id="checkbox-{{ servicename }}-ingoing"
            value="portIn"
          />
          Ingoing
        </label>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-going"
            id="checkbox-{{ servicename }}-outgoing"
            value="portOut"
          />
          Outgoing
        </label>
      </div>
      <div id="service-configuration-status">
        For which storage, do you want to use this service?
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-property"
            id="checkbox-{{ servicename }}-filestorage"
            value="fileStorage"
          />
          File Storage
        </label>
        <label>
          <input
            type="checkbox"
            name="checkbox-{{ servicename }}-property"
            id="checkbox-{{ servicename }}-metadata"
            value="metadata"
          />
          Metadata Storage
        </label>
      </div>
    </div>
  </div>
  {{/each}}
</div>

<div id="wrapper-custom-buttons">
  <button id="btn-add-new-service">Add new service</button>
  <div id="spacer"></div>
  <button id="btn-save-research">Save</button>
  <button id="btn-save-research-and-continue">Save & continue</button>
</div>
