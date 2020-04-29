(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.Files = function (baseUrl) {
    this._baseUrl = baseUrl;
    this._userId = OC.currentUser;
  };

  OC.rds.Files.prototype = {
    triggerUpload: function (researchIndex, filename) {
      var deferred = $.Deferred();

      var data = { filename: filename };

      $.ajax({
        type: "POST",
        url: OC.generateUrl("/apps/rds/research/files"),
        data: JSON.stringify(data),
        dataType: "json",
      })
        .done(function () {
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
  };
})(OC, window, jQuery);
