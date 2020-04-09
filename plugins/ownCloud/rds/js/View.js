(function (OC, window, $, undefined) {
  "use strict";

  var translations = {
    newresearch: $("#new-research-string").text(),
  };

  OC.rds = OC.rds || {};

  OC.rds.View = function (studies, services, files) {
    this._studies = studies;
    this._services = services;
    this._files = files;
    this._stateView = undefined;
  };

  OC.rds.View.prototype = {
    renderContent: function () {
      var self = this;

      saveFunction = function () {
        console.log("nothing todo in saveFunction");
        // self.metadata.saveCurrent()
        return $.when();
      };

      function saveCurrentServiceInformations() {
        var portIn = [];
        var portOut = [];

        this._services.forEach((element) => {
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
            function () {
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
            $('input[id="checkbox-' + element.servicename + '-ingoing"]').prop(
              "checked"
            )
          ) {
            portIn.push(tempPortIn);
          }

          if (
            $('input[id="checkbox-' + element.servicename + '-outgoing"]').prop(
              "checked"
            )
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
        services: this._services.getAll(),
      });

      $("#app-content").html(html);

      function saveCurrentState() {
        saveFunction()
          .done(function () {
            self.render();
          })
          .fail(function () {
            alert("Could not update research, not found");
          });
      }

      $("#app-content button #btn-save-research").click(function () {
        saveCurrentState();
      });

      $("#app-content button #btn-save-research-and-continue").click(
        function () {
          self._stateView += 1;
          saveCurrentState();
        }
      );
    },
    renderNavigation: function () {
      var source = $("#navigation-tpl").html();
      var template = Handlebars.compile(source);
      var html = template({ studies: this._studies.getAll() });

      $("#app-navigation ul").html(html);

      // create new research
      var self = this;
      $("#new-research").click(function () {
        var conn = {};

        self._studies
          .create()
          .done(function () {
            self.render();
          })
          .fail(function () {
            alert("Could not create research");
          });
      });

      // show app menu
      $("#app-navigation .app-navigation-entry-utils-menu-button").click(
        function () {
          var entry = $(this).closest(".research");
          entry.find(".app-navigation-entry-menu").toggleClass("open");
        }
      );

      // delete a research
      $("#app-navigation .research .delete").click(function () {
        var entry = $(this).closest(".research");
        entry.find(".app-navigation-entry-menu").removeClass("open");

        self._studies
          .removeActive()
          .done(function () {
            self.render();
          })
          .fail(function () {
            alert("Could not delete research, not found");
          });
      });

      // load a research
      $("#app-navigation .research > a").click(function () {
        var id = parseInt($(this).parent().data("id"), 10);
        self._studies.load(id);
        self.render();
      });
    },
    render: function () {
      this.renderNavigation();
      this.renderContent();
    },
    loadAll: function () {
      var self = this;

      return $.when(
        self._studies.loadAll(),
        self._services.loadAll()
        // needed later
        //self._files.loadAll()
      );
    },
  };
})(OC, window, jQuery);
