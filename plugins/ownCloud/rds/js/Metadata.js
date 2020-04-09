(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.Metadata = function (baseUrl) {
    this._baseUrl = baseUrl;
    this._metadata = [];
    this._activeResearchId = undefined;
  };

  OC.rds.Metadata.prototype = {
    load: function (id) {
      var deferred = $.Deferred();
      var self = this;
      $.get(this._baseUrl)
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
    update: function (metadata) {
      var self = this;
      var md = {};
      md.metadataArr = metadata;

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
