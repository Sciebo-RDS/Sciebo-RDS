(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.Studies = function (metadata) {
    this._baseUrl = OC.generateUrl("/apps/rds/research");
    this._studies = [];
    this._activeResearch = undefined;
    this._metadata = metadata;
  };

  OC.rds.Studies.prototype = {
    load: function (researchIndex) {
      var self = this;
      this._studies.forEach(function (conn) {
        if (conn.researchIndex === researchIndex) {
          conn.active = true;
          self._activeResearch = conn;
        } else {
          conn.active = false;
        }
      });
    },
    getActive: function () {
      return this._activeResearch;
    },
    getActiveMetadata: function () {
      return this._metadata;
    },
    loadMetadata: function () {
      return this._metadata.load(this._activeResearch.researchIndex);
    },

    publishActive: function(){
      var index = undefined;
      var deferred = $.Deferred();
      var researchIndex = this._activeResearch.researchIndex;

      this._studies.forEach(function (conn, counter) {
        if (conn.researchIndex === researchIndex) {
          index = counter;
        }
      });

      if (index !== undefined) {
        if (this._activeResearch === this._studies[index]) {
          delete this._activeResearch;
        }

        this._studies.splice(index, 1);

        $.ajax({
          url: this._baseUrl + "/" + researchIndex + "/publish",
          method: "POST",
        })
          .done(function () {
            deferred.resolve();
          })
          .fail(function () {
            deferred.reject();
          });
      } else {
        deferred.reject();
      }
      return deferred.promise();
    },
    removeActive: function () {
      var index = undefined;
      var deferred = $.Deferred();
      var researchIndex = this._activeResearch.researchIndex;

      this._studies.forEach(function (conn, counter) {
        if (conn.researchIndex === researchIndex) {
          index = counter;
        }
      });

      if (index !== undefined) {
        if (this._activeResearch === this._studies[index]) {
          delete this._activeResearch;
        }

        this._studies.splice(index, 1);

        $.ajax({
          url: this._baseUrl + "/" + researchIndex,
          method: "DELETE",
        })
          .done(function () {
            deferred.resolve();
          })
          .fail(function () {
            deferred.reject();
          });
      } else {
        deferred.reject();
      }
      return deferred.promise();
    },
    create: function () {
      var deferred = $.Deferred();
      var self = this;
      $.ajax({
        url: this._baseUrl,
        method: "POST",
      })
        .done(function (conn) {
          self._studies.push(conn);
          self._activeResearch = conn;
          self.load(conn.researchIndex);
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    getAll: function () {
      return this._studies;
    },
    loadAll: function () {
      var deferred = $.Deferred();
      var self = this;
      $.get(this._baseUrl)
        .done(function (conns) {
          self._activeResearch = undefined;
          self._studies = [];
          conns.forEach(function (conn, counter) {
            if (conn.status < 3) {
              self._studies.push(conn);
            }
          });
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    save: function () {
      var deferred = $.Deferred();

      var conn = this._activeResearch;

      $.ajax({
        url: this._baseUrl + "/" + conn.researchIndex,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify(conn),
      })
        .done(function () {
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
    updateActive: function (portIn, portOut) {
      var conn = this._activeResearch;

      conn.portIn = portIn;
      conn.portOut = portOut;
      conn.status = 2;

      this._activeResearch = conn;

      return this.save();
    },
  };
})(OC, window, jQuery);
