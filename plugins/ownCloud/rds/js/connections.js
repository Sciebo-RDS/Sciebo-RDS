// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js
(function(OC, window, $, undefined) {
  "use strict";

  $(document).ready(function() {
    var translations = {
      newNote: $("#new-connection-string").text()
    };

    var Metadata = function(baseUrl) {
      this._baseUrl = baseUrl;
      this._metadata = [];
    };

    var Files = function(baseUrl) {
      this._baseUrl = baseUrl;
    };

    var Connections = function(baseUrl) {
      this._baseUrl = baseUrl;
      this._connections = [];
      this._activeConnection = undefined;
    };

    Connections.prototype = {
      load: function(id) {
        var self = this;
        this._connections.forEach(function(conn) {
          if (conn.id === id) {
            conn.active = true;
            self._activeConnection = conn;
          } else {
            conn.active = false;
          }
        });
      },
      getActive: function() {
        return this._activeConnection;
      },
      removeActive: function() {
        var index;
        var deferred = $.Deferred();
        var id = this._activeConnection.id;

        this._connections.forEach(function(conn, counter) {
          if (conn.id === id) {
            index = counter;
          }
        });

        if (index !== undefined) {
          if (this._activeConnection === this._connections[index]) {
            delete this._activeConnection;
          }

          this._connections.splice(index, 1);

          $.ajax({
            url: this._baseUrl + "/" + id,
            method: "DELETE"
          })
            .done(function() {
              deferred.resolve();
            })
            .fail(function() {
              deferred.reject();
            });
        } else {
          deferred.reject();
        }
        return deferred.promise();
      },
      create: function() {
        var deferred = $.Deferred();
        var self = this;
        $.ajax({
          url: this._baseUrl,
          method: "POST"
        })
          .done(function(conn) {
            self._connections.push(conn);
            self._activeConnection = conn;
            self.load(conn.id);
            deferred.resolve();
          })
          .fail(function() {
            deferred.reject();
          });
        return deferred.promise();
      },
      getAll: function() {
        return this._connections;
      },
      loadAll: function() {
        var deferred = $.Deferred();
        var self = this;
        $.get(this._baseUrl)
          .done(function(conns) {
            self._activeConnection = undefined;
            self._connections = conns;
            deferred.resolve();
          })
          .fail(function() {
            deferred.reject();
          });
        return deferred.promise();
      },
      updateActive: function(projectIndex, status, portIn, portOut) {
        var conn = this.getActive();

        conn.projectIndex = projectIndex;
        conn.status = status;
        conn.portIn = portIn;
        conn.portOut = portOut;

        return $.ajax({
          url: this._baseUrl + "/" + conn.id,
          method: "PUT",
          contentType: "application/json",
          data: JSON.stringify(conn)
        });
      }
    };

    var View = function(connections, metadata, files) {
      this._connections = connections;
      this._metadata = metadata;
      this._files = files;
      this._stateView = undefined;
    };

    View.prototype = {
      renderContent: function() {
        saveFunction = function() {
          console.log("nothing todo in saveFunction");
          return $.when();
        };

        loadId = "#connection-overview-tpl";
        if (self._activeConnection !== undefined) {
          switch (self._stateView) {
            case 2:
              loadId = "#connection-edit-metadata-tpl";
              break;
            case 3:
              loadId = "#connection-edit-file-tpl";
              break;
            default:
              self._stateView = 1;
              saveFunction = self._connections.updateActive;
              loadId = "#connection-edit-service-tpl";
          }
        }

        var source = $(loadId).html();
        var template = Handlebars.compile(source);
        var html = template({ connection: this._connections.getActive() });

        $("#app-content").html(html);

        var self = this;

        // TODO: add a function, which edits the activeConnection to the new values

        // TODO: handle saves
        function saveCurrentState() {
          saveFunction()
            .done(function() {
              self.render();
            })
            .fail(function() {
              alert("Could not update connection, not found");
            });
        }

        $("#app-content button #btn-save-connection").click(function() {
          saveCurrentState();
        });

        $("#app-content button #btn-save-connection-and-continue").click(
          function() {
            self._stateView += 1;
            saveCurrentState();
          }
        );
      },
      renderNavigation: function() {
        var source = $("#navigation-tpl").html();
        var template = Handlebars.compile(source);
        var html = template({ connections: this._connections.getAll() });

        $("#app-navigation ul").html(html);

        // create new note
        var self = this;
        $("#new-connection").click(function() {
          var conn = {};

          self._connections
            .create()
            .done(function() {
              self.render();
            })
            .fail(function() {
              alert("Could not create note");
            });
        });

        // show app menu
        $("#app-navigation .app-navigation-entry-utils-menu-button").click(
          function() {
            var entry = $(this).closest(".connection");
            entry.find(".app-navigation-entry-menu").toggleClass("open");
          }
        );

        // delete a note
        $("#app-navigation .connection .delete").click(function() {
          var entry = $(this).closest(".connection");
          entry.find(".app-navigation-entry-menu").removeClass("open");

          self._connections
            .removeActive()
            .done(function() {
              self.render();
            })
            .fail(function() {
              alert("Could not delete connection, not found");
            });
        });

        // load a note
        $("#app-navigation .connection > a").click(function() {
          var id = parseInt(
            $(this)
              .parent()
              .data("id"),
            10
          );
          self._connections.load(id);
          self.render();
        });
      },
      render: function() {
        this.renderNavigation();
        this.renderContent();
      },
      loadAll: function() {
        var self = this;

        return $.when(
          self._connections.loadAll()
          // needed later
          //self._metadata.loadAll(),
          //self._files.loadAll()
        );
      }
    };

    var connections = new Connections(OC.generateUrl("/apps/rds/connections"));
    var metadata = new Metadata(undefined);
    var files = new Metadata(undefined);

    var view = new View(connections, metadata, files);
    view
      .loadAll()
      .done(function() {
        view.render();
      })
      .fail(function() {
        alert("Could not load informations");
      });
  });
})(OC, window, jQuery);
