// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js
(function(OC, window, $, undefined) {
  "use strict";

  $(document).ready(function() {
    var translations = {
      newNote: $("#new-research-string").text()
    };

    var Metadata = function(baseUrl) {
      this._baseUrl = baseUrl;
      this._metadata = [];
    };

    var Files = function(baseUrl) {
      this._baseUrl = baseUrl;
    };

    var Services = function(baseUrl) {
      this._baseUrl = baseUrl;
      this._services = [];
    };

    Services.prototype = {
      loadAll: function() {
        var deferred = $.Deferred();
        var self = this;

        $.get(this._baseurl + "/user/service", "json")
          .done(function(services) {
            self._services = services;
            deferred.resolve();
          })
          .fail(function() {
            deferred.reject();
          });
        return deferred.promise();
      },
      getAll: function() {
        return self._services;
      }
    };

    var Studies = function(baseUrl) {
      this._baseUrl = baseUrl;
      this._studies = [];
      this._activeResearch = undefined;
    };

    Studies.prototype = {
      load: function(id) {
        var self = this;
        this._studies.forEach(function(conn) {
          if (conn.id === id) {
            conn.active = true;
            self._activeResearch = conn;
          } else {
            conn.active = false;
          }
        });
      },
      getActive: function() {
        return this._activeResearch;
      },
      removeActive: function() {
        var index;
        var deferred = $.Deferred();
        var id = this._activeResearch.id;

        this._studies.forEach(function(conn, counter) {
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
            self._studies.push(conn);
            self._activeResearch = conn;
            self.load(conn.id);
            deferred.resolve();
          })
          .fail(function() {
            deferred.reject();
          });
        return deferred.promise();
      },
      getAll: function() {
        return this._studies;
      },
      loadAll: function() {
        var deferred = $.Deferred();
        var self = this;
        $.get(this._baseUrl)
          .done(function(conns) {
            self._activeResearch = undefined;
            self._studies = conns;
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

    var View = function(connections, services, metadata, files) {
      this._studies = connections;
      this._services = services;
      this._metadata = metadata;
      this._files = files;
      this._stateView = undefined;
    };

    View.prototype = {
      renderContent: function() {
        var self = this;

        saveFunction = function() {
          console.log("nothing todo in saveFunction");
          // self.metadata.saveCurrent()
          return $.when();
        };

        function saveCurrentServiceInformations() {
          var portIn = [];
          var portOut = [];

          this._services.forEach(element => {
            var properties = [];

            var value = $(
              "input[name='radiobutton-" + element.servicename + "']:checked"
            ).val();

            tempPortIn["port"] = element.servicename;
            tempPortOut["port"] = element.servicename;

            var propertyProjectInService = {};
            propertyProjectInService["key"] = "projectName";
            propertyProjectInService["value"] = value;
            properties.push(propertyProjectInService);

            $.each(
              $(
                "input[name='checkbox-" +
                  element.servicename +
                  "-property']:checked"
              ),
              function() {
                var val = $(this).val();

                var property = {};
                property["portType"] = val;
                property["value"] = true;
                properties.push(property);
              }
            );

            tempPortIn["properties"] = properties;
            tempPortOut["properties"] = properties;

            if (
              $(
                'input[id="checkbox-' + element.servicename + '-ingoing"]'
              ).prop("checked")
            ) {
              portIn.push(tempPortIn);
            }

            if (
              $(
                'input[id="checkbox-' + element.servicename + '-outgoing"]'
              ).prop("checked")
            ) {
              portOut.push(tempPortOut);
            }
          });

          var projectIndex = self._studies.getActive().projectIndex;
          var status = self._studies.getActive().status;

          self._studies.updateActive(projectIndex, status, portIn, portOut);
        }

        loadView = "#research-overview-tpl";
        if (self._activeResearch !== undefined) {
          switch (self._stateView) {
            case 2:
              loadView = "#research-edit-metadata-tpl";
              break;
            case 3:
              loadView = "#research-edit-file-tpl";
              break;
            default:
              self._stateView = 1;
              saveFunction = saveCurrentServiceInformations;
              loadView = "#research-edit-service-tpl";
          }
        }

        var source = $(loadView).html();
        var template = Handlebars.compile(source);
        var html = template({
          research: this._studies.getActive(),
          services: this._services.getAll()
        });

        $("#app-content").html(html);

        function saveCurrentState() {
          saveFunction()
            .done(function() {
              self.render();
            })
            .fail(function() {
              alert("Could not update research, not found");
            });
        }

        $("#app-content button #btn-save-research").click(function() {
          saveCurrentState();
        });

        $("#app-content button #btn-save-research-and-continue").click(
          function() {
            self._stateView += 1;
            saveCurrentState();
          }
        );
      },
      renderNavigation: function() {
        var source = $("#navigation-tpl").html();
        var template = Handlebars.compile(source);
        var html = template({ connections: this._studies.getAll() });

        $("#app-navigation ul").html(html);

        // create new note
        var self = this;
        $("#new-research").click(function() {
          var conn = {};

          self._studies
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
            var entry = $(this).closest(".research");
            entry.find(".app-navigation-entry-menu").toggleClass("open");
          }
        );

        // delete a note
        $("#app-navigation .research .delete").click(function() {
          var entry = $(this).closest(".research");
          entry.find(".app-navigation-entry-menu").removeClass("open");

          self._studies
            .removeActive()
            .done(function() {
              self.render();
            })
            .fail(function() {
              alert("Could not delete research, not found");
            });
        });

        // load a note
        $("#app-navigation .research > a").click(function() {
          var id = parseInt(
            $(this)
              .parent()
              .data("id"),
            10
          );
          self._studies.load(id);
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
          self._studies.loadAll(),
          self._services.loadAll()
          // needed later
          //self._metadata.loadAll(),
          //self._files.loadAll()
        );
      }
    };

    var connections = new Studies(OC.generateUrl("/apps/rds/connections"));
    var services = new Services(OC.generateUrl("/apps/rds/connections"));
    var metadata = new Metadata(undefined);
    var files = new Files(undefined);

    var view = new View(connections, services, metadata, files);
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
