(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    var Services = function (baseUrl) {
      this._baseUrl = baseUrl;
      this._services = [];
    };
    
    Services.prototype = {
      loadAll: function () {
        var deferred = $.Deferred();
        var self = this;

        $.get(this._baseurl + "/user", "json")
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
  });
})(OC, window, jQuery);
