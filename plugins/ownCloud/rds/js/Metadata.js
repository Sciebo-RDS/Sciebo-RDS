(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.Metadata = function () {
    this._baseUrl = OC.generateUrl("/apps/rds/metadata");
    this._metadata = [];
    this._schema = undefined;
    this._version = undefined;
    this._activeResearchId = undefined;
  };

  OC.rds.Metadata.prototype = {
    loadJsonSchema: function () {
      var deferred = $.Deferred();
      var self = this;
      $.get(this._baseUrl + "/jsonschema")
        .done(function (schema) {
          var rdsJSON = JSON.parse(schema);

          self._version = rdsJSON.kernelversion;
          self._schema = JSON.parse(rdsJSON.schema);

          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    getMetadata: function () {
      return this._metadata;
    },
    getSchema: function () {
      return this._schema;
    },
    load: function (id) {
      var deferred = $.Deferred();
      var self = this;
      $.get(this._baseUrl + "/" + id)
        .done(function (metadatas) {
          self._metadata = metadatas;
          self._activeResearchId = id;
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    update: function (metadataDict) {
      var self = this;
      var md = {};
      md.metadataArr = metadataDict;

      return $.ajax({
        url: this._baseUrl + "/" + this._activeResearchId,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify(md),
        success: function (metadatas) {
          self._metadata = metadatas;
        },
      });
    },
  };
})(OC, window, jQuery);
