(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.Services = function () {
    this._userservices = [];
    this._services = [];
  };

  OC.rds.Services.prototype = {
    loadAll: function () {
      return $.when(this.loadUser(), this.loadService());
    },
    loadUser: function () {
      var deferred = $.Deferred();
      var self = this;

      $.get(OC.generateUrl("/apps/rds/userservice"))
        .done(function (services) {
          self._userservices = services;
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    loadService: function () {
      var deferred = $.Deferred();
      var self = this;

      $.get(OC.generateUrl("/apps/rds/service"))
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
      return this._userservices;
    },
    getServices: function () {
      return this._services;
    },
  };
})(OC, window, jQuery);
