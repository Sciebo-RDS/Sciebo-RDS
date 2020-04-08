(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    var Studies = function (baseUrl) {
      this._baseUrl = baseUrl;
      this._studies = [];
      this._activeResearch = undefined;
    };

    Studies.prototype = {
      load: function (id) {
        var self = this;
        this._studies.forEach(function (conn) {
          if (conn.id === id) {
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
      removeActive: function () {
        var index;
        var deferred = $.Deferred();
        var id = this._activeResearch.id;

        this._studies.forEach(function (conn, counter) {
          if (conn.id === id) {
            index = counter;
          }
        });

        if (index !== undefined) {
          if (this._activeResearch === this._studies[index]) {
            delete this._activeResearch;
          }

          this._studies.splice(index, 1);

          $.ajax({
            url: this._baseUrl + "/" + id,
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
            self.load(conn.id);
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
            self._studies = conns;
            deferred.resolve();
          })
          .fail(function () {
            deferred.reject();
          });
        return deferred.promise();
      },
      updateActive: function (projectIndex, status, portIn, portOut) {
        var conn = this.getActive();

        conn.projectIndex = projectIndex;
        conn.status = status;
        conn.portIn = portIn;
        conn.portOut = portOut;

        return $.ajax({
          url: this._baseUrl + "/" + conn.id,
          method: "PUT",
          contentType: "application/json",
          data: JSON.stringify(conn),
        });
      },
    };
  });
})(OC, window, jQuery);
