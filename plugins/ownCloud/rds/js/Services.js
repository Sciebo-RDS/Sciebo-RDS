(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.Services = function (baseUrl) {
    this._baseUrl = baseUrl;
    this._services = [];
  };

  OC.rds.Services.prototype = {
    loadAll: function () {
      var deferred = $.Deferred();
      var self = this;

      $.get(this._baseurl, "json")
        .done(function (services) {
          self._services = services;
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    getAll: function () {
      return self._services;
    },
  };
})(OC, window, jQuery);
