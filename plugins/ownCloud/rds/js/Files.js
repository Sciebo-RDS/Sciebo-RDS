(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.Files = function () {
    this._baseUrl = OC.generateUrl("/apps/rds/research/files");
    this._userId = OC.currentUser;
    this._settings = undefined;
    this._currentFiles = [];
    this._currentResearch = undefined;
  };

  OC.rds.Files.prototype = {
    load: function (researchIndex) {
      var self = this;
      $.when(
        this.loadSettings(researchIndex),
        this.loadFiles(researchIndex)
      ).then(function () {
        self._currentResearch = researchIndex;
      });
    },
    triggerSync: function () {
      var deferred = $.Deferred();

      if (this._currentResearch === undefined) {
        deferred.reject();
        return deferred.promise();
      }

      $.ajax({
        type: "POST",
        url: OC.generateUrl(
          "/apps/rds/research/" + this._currentResearch + "/files"
        ),
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
    triggerUpload: function (filename) {
      var deferred = $.Deferred();

      var data = { filename: filename };

      if (this._currentResearch === undefined) {
        deferred.reject();
        return deferred.promise();
      }

      $.ajax({
        type: "POST",
        url: OC.generateUrl(
          "/apps/rds/research/" + this._currentResearch + "/files"
        ),
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
    triggerRemove: function (filename) {},
    loadSettings: function (researchIndex) {
      var deferred = $.Deferred();
      var self = this;

      $.ajax({
        type: "GET",
        url: OC.generateUrl(
          "/apps/rds/research/" + researchIndex + "/settings"
        ),
        dataType: "json",
      })
        .done(function (settings) {
          self._settings = settings;
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    saveSettings: function () {
      var deferred = $.Deferred();

      var data = { settings: this._settings };

      $.ajax({
        type: "PUT",
        url: OC.generateUrl(
          "/apps/rds/research/" + this._currentResearch + "/settings"
        ),
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
    getFiles: function () {
      return this._currentFiles;
    },
    getCurrentResearch: function () {
      return this._currentResearch;
    },
    loadFiles: function (researchIndex) {
      var deferred = $.Deferred();
      var self = this;

      $.ajax({
        type: "GET",
        url: OC.generateUrl("/apps/rds/research/" + researchIndex + "/files"),
        dataType: "json",
      })
        .done(function (files) {
          self._currentFiles = files;
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
  };
})(OC, window, jQuery);
