(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  OC.rds.AbstractTemplate = function (divName, view) {
    this._divName = divName;
    this._view = view;

    if (this.constructor === OC.rds.AbstractTemplate) {
      throw new Error("Cannot instanciate abstract class");
    }
  };

  OC.rds.AbstractTemplate.prototype = {
    // this methods needs to be implemented in your inherited classes
    // returns a dict
    _getParams: function () {
      throw new Error("You have to implement the method _getParams!");
    },
    // returns a jquery Differed object
    _saveFn: function () {
      throw new Error("You have to implement the method _saveFn!");
    },
    // returns nothing
    _beforeTemplateRenders: function () {
      throw new Error(
        "You have to implement the method _beforeTemplateRenders!"
      );
    },
    // returns nothing
    _afterTemplateRenders: function () {
      throw new Error(
        "You have to implement the method _afterTemplateRenders!"
      );
    },

    _loadTemplate: function () {
      var source = $(this._divName).html();
      var template = Handlebars.compile(source);
      var html = template(this._getParams());

      $("#app-content-wrapper").html(html);
    },

    render: function () {
      this._beforeTemplateRenders();
      this._loadTemplate();
      this._afterTemplateRenders();
    },

    save: function () {
      return this._saveFn()
        .fail(function () {
          OC.dialogs.alert(
            t("rds", "Your entries could not be saved."),
            t("rds", "RDS Update project")
          );
        });
    },

    save_next: function () {
      var self = this;

      return this.save().done(function () {
        self._view._stateView += 1;
        self._view.render();
      });
    },
  };

  OC.rds.OverviewTemplate = function (divName, view, services, studies) {
    OC.rds.AbstractTemplate.call(this, divName, view);

    this._services = services;
    this._studies = studies;
  };

  OC.rds.OverviewTemplate.prototype = Object.create(
    OC.rds.AbstractTemplate.prototype,
    {
      constructor: OC.rds.OverviewTemplate,
    }
  );

  OC.rds.OverviewTemplate.prototype._getParams = function () {
    return {
      studies: this._studies.getAll(),
      services: this._services.getAll(),
    };
  };
  OC.rds.OverviewTemplate.prototype._beforeTemplateRenders = function () { };
  OC.rds.OverviewTemplate.prototype._afterTemplateRenders = function () { };
  OC.rds.OverviewTemplate.prototype._saveFn = function () {
    $.when();
  };

  OC.rds.ServiceTemplate = function (divName, view, services, studies) {
    OC.rds.AbstractTemplate.call(this, divName, view);

    this._services = services;
    this._studies = studies;
  };

  OC.rds.ServiceTemplate.prototype = Object.create(
    OC.rds.AbstractTemplate.prototype,
    {
      constructor: OC.rds.ServiceTemplate,
    }
  );
  OC.rds.ServiceTemplate.prototype._getParams = function () {
    var self = this;

    var patchServices = function (services, research) {
      var newServices = JSON.parse(JSON.stringify(services));

      function findPort(portName, portList) {
        var searchName = portName;

        if (!searchName.startsWith("port-")) {
          searchName = "port-" + searchName.toLowerCase();
        }

        var port = {};
        portList.forEach(function (elem) {
          if (elem.port === searchName) {
            this.port = elem;
          }
        }, port);
        return port.port;
      }

      newServices.forEach(function (service, indexSvc) {
        function patchProperty(prop) {
          if (prop.portType === "metadata" && prop.value === true) {
            this[indexSvc].metadataChecked = "checked";
          }
          if (prop.portType === "fileStorage" && prop.value === true) {
            this[indexSvc].fileStorageChecked = "checked";
          }

          if (prop.portType === "customProperties") {
            prop.value.forEach(function (val) {
              if (val.key === "filepath") {
                this[indexSvc].filepath = val.value;
              }

              service.serviceProjects.forEach(function (proj, indexProj) {
                if (
                  val.key === "projectId" &&
                  val.value === proj.metadata.prereserve_doi.recid.toString()
                ) {
                  this[indexSvc].serviceProjects[indexProj].checked = "checked";
                }
              }, this);
            }, this);
          }
        }

        var port = findPort(service.servicename, research.portIn);
        if (port !== undefined) {
          this[indexSvc].importChecked = "checked";

          port.properties.forEach(patchProperty, this);
        }

        port = findPort(service.servicename, research.portOut);
        if (port !== undefined) {
          this[indexSvc].exportChecked = "checked";
          port.properties.forEach(patchProperty, this);
        }
      }, newServices);

      return newServices;
    };

    function staticServices(services, research) {
      var newServices = JSON.parse(JSON.stringify(services));

      newServices.forEach(function (service, indexSvc) {
        if (service.servicename === "Owncloud") {
          this[indexSvc].fileStorageChecked = "checked";
          this[indexSvc].importChecked = "checked";
        }

        if (service.servicename === "Zenodo") {
          this[indexSvc].metadataChecked = "checked";
          this[indexSvc].exportChecked = "checked";
        }
      }, newServices);

      return newServices;
    }

    var studies = this._studies.getActive();
    var services;

    if (studies === undefined) {
      services = [];
    } else {
      services = patchServices(this._services.getAll(), studies);
      services = staticServices(services, studies);
    }

    return {
      research: studies,
      services: services,
    };
  };
  OC.rds.ServiceTemplate.prototype._beforeTemplateRenders = function () { };
  OC.rds.ServiceTemplate.prototype._afterTemplateRenders = function () {
    var self = this;

    var btn = $("#btn-open-folderpicker");
    var servicename = btn.data("service");

    $("[class=service-configuration]").hide();
    //$("#btn-save-research-and-continue").hide();
    //$("#btn-sync-files-in-research").hide();

    btn.click(function () {
      OC.dialogs.filepicker(
        t("files", "Choose source and / or target folder"),
        function (targetPath, type) {
          $("#fileStorage-path-" + servicename).html(targetPath);
          self._services.getAll().forEach(function (element, index) {
            if (element.servicename === servicename) {
              this[index].filepath = targetPath.trim();
            }
          }, self._services.getAll());
          self._view.render();
        },
        false,
        "httpd/unix-directory",
        true
      );
    });


    $("#app-content-wrapper #btn-save-research").click(function () {
      self.save()
    });

    $("#app-content-wrapper #btn-save-research-and-continue").click(function () {
      self.save_next();
    });
  };

  OC.rds.ServiceTemplate.prototype._saveFn = function () {
    var self = this;
    self.data = {};

    var checkIfProjectCreate = function () {
      var btns = $(".radiobutton-new-project");
      var deferreds = [];
      console.log(btns);

      function createProject(servicename, radio) {
        var deferred = $.Deferred();
        $.ajax({
          url: OC.generateUrl(
            "/apps/rds/userservice/" + servicename + "/projects"
          ),
          method: "POST",
        })
          .done(function (proj) {
            console.log(proj);
            radio.data("value", proj.projectId);
            self._services.loadUser().done(function () {
              self._view.render();
              var btn = $($("input[name='radiobutton-" + servicename + "']")[0])
              btn.prop("checked", true);
              btn.data("value", proj.projectId);
              self.data[servicename] = proj.projectId;
              console.log("projectId in self.data " + servicename + ": " + self.data[servicename]);
            }).always(function () {
              deferred.resolve(proj.projectId);
            })
          })
          .fail(function () {
            deferred.reject();
          });
        return deferred.promise();
      }

      btns.each(function () {
        var $this = $(this);

        if ($this.is(":checked")) {
          var servicename = $this.data("servicename");
          console.log(servicename);
          deferreds.push(createProject(servicename, $this));
        }
      });

      return $.when.apply($, deferreds);
    }

    return checkIfProjectCreate().then(function () {
      var portIn = [];
      var portOut = [];

      self._services.getAll().forEach(function (element) {
        var properties = [];
        var tempPortIn = {};
        var tempPortOut = {};

        var portName = element.servicename;
        if (!portName.startsWith("port-")) {
          portName = "port-" + portName.toLowerCase();
        }

        tempPortIn["port"] = portName;
        tempPortOut["port"] = portName;

        var valProp = [];

        var tmpRadio = $("input[name='radiobutton-" + element.servicename + "']:checked");
        var projectId = tmpRadio.data("value");
        console.log("projectId " + projectId)
        console.log(self.data)

        if ((projectId === "on" || typeof projectId === "undefined") && element.servicename in self.data) {
          projectId = self.data[element.servicename]
          console.log("projectId in self.data " + element.servicename + ": " + self.data[servicename]);
        }
        console.log("projectId " + projectId)

        if (projectId !== undefined) {
          valProp.push({
            key: "projectId",
            value: projectId.toString(),
          });
        }

        console.log(valProp)

        var filePathObj = $("#fileStorage-path-" + element.servicename);
        if (filePathObj.length) {
          var filepath = filePathObj.html().trim();
          if (filepath !== undefined) {
            valProp.push({
              key: "filepath",
              value: filepath,
            });
          }
        }

        properties.push({
          portType: "customProperties",
          value: valProp,
        });

        $.each(
          $(
            "input[name='checkbox-" + element.servicename + "-property']:checked"
          ),
          function () {
            var val = $(this).data("value");

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
          ) === true
        ) {
          portIn.push(tempPortIn);
        }

        if (
          $('input[id="checkbox-' + element.servicename + '-outgoing"]').prop(
            "checked"
          ) === true
        ) {
          portOut.push(tempPortOut);
        }
      });

      return self._studies.updateActive(portIn, portOut)
    });
  };

  OC.rds.MetadataTemplate = function (divName, view, studies, services) {
    OC.rds.AbstractTemplate.call(this, divName, view);

    this._studies = studies;
    this._services = services;
    this._bf = undefined;
  };

  OC.rds.MetadataTemplate.prototype = Object.create(
    OC.rds.AbstractTemplate.prototype,
    {
      constructor: OC.rds.MetadataTemplate,
    }
  );
  OC.rds.MetadataTemplate.prototype._beforeTemplateRenders = function () { };
  OC.rds.MetadataTemplate.prototype._afterTemplateRenders = function () {
    var self = this;

    this._studies.loadMetadata().done(function () {
      var data = self._studies._metadata.getMetadata()[0]["metadata"];
      console.log(data);

      var BrutusinForms = brutusin["json-forms"];
      self._bf = BrutusinForms.create(self._studies._metadata.getSchema());
      var container = document.getElementById("metadata-jsonschema-editor");
      container.innerHTML = "";
      self._bf.render(container, data);
    });

    $("#app-content-wrapper #btn-save-metadata").click(function () {
      self.save();
    });

    $("#app-content-wrapper #btn-save-metadata-and-continue").click(function () {
      self.save_next();
    });

    $("#app-content-wrapper #btn-skip").click(function () {
      self._view._stateView += 1;
      self._view.render();
    });
  };
  OC.rds.MetadataTemplate.prototype._getParams = function () { };
  OC.rds.MetadataTemplate.prototype._saveFn = function () {
    var self = this;
    if (self._bf === undefined || !self._bf.validate()) {
      var deferred = $.Deferred();
      deferred.reject();
      return deferred.promise();
    }

    return self._studies._metadata.update(self._bf.getData()).done(function () { self._services.loadUser() });
  };

  OC.rds.FileTemplate = function (divName, view, services, studies, files) {
    OC.rds.AbstractTemplate.call(this, divName, view);
    this._services = services;
    this._studies = studies;
    this._files = files;
  };
  OC.rds.FileTemplate.prototype = Object.create(
    OC.rds.AbstractTemplate.prototype,
    {
      constructor: OC.rds.FileTemplate,
    }
  );

  OC.rds.FileTemplate.prototype._beforeTemplateRenders = function () {
    this._files.load(this._studies.getActive().researchIndex);
  };
  OC.rds.FileTemplate.prototype._afterTemplateRenders = function () {
    var self = this;

    $(".wrapper-auto-upload").hide();
    $(".wrapper-apply-changes").hide();
    $("#btn-save-files").hide();

    $("#btn-save-files").click(function () {
      self.save();
    });

    $("#btn-sync-files").click(function () {

      self._view._files.load(self._studies.getActive().researchIndex);
      self._view._files.triggerSync().done(function () {
        console.log("done")
      });

      OC.dialogs.alert(
        t("rds", "Your files will be synchronize within 2 minutes."),
        t("rds", "RDS Update project")
      );
    });

    $("#btn-finish-research").click(function () {
      OC.dialogs.confirm(
        t("rds", "Are you sure, that you want to close the research {researchIndex}?", {
          researchIndex: self._studies.getActive().researchIndex + 1,
        }),
        t("rds", "RDS Update project"),
        function (confirmation) {
          {
            if (confirmation == false) {
              return;
            }

            self._studies
              .publishActive()
              .done(function () {
                self._view._stateView = 0;
                self._view.render();
              })
              .fail(function () {
                OC.dialogs.alert(
                  t("rds", "Could not close this research."),
                  t("rds", "RDS Update project")
                );
              });
          }
        }
      );
    });
  };
  OC.rds.FileTemplate.prototype._getParams = function () { };
  OC.rds.FileTemplate.prototype._saveFn = function () {
    return $.when();
  };

  OC.rds.View = function (studies, services, files) {
    this._studies = studies;
    this._services = services;
    this._files = files;
    this._stateView = 0;

    this._templates = [
      new OC.rds.OverviewTemplate(
        "#research-overview-tpl",
        this,
        this._services,
        this._studies
      ),
      new OC.rds.ServiceTemplate(
        "#research-edit-service-tpl",
        this,
        this._services,
        this._studies
      ),
      new OC.rds.MetadataTemplate(
        "#research-edit-metadata-tpl",
        this,
        this._studies,
        this._services
      ),
      new OC.rds.FileTemplate(
        "#research-edit-file-tpl",
        this,
        this._services,
        this._studies,
        this._files
      ),
    ];
  };

  OC.rds.View.prototype = {
    renderContent: function () {
      var self = this;
      if (self._studies.getActive() === undefined) {
        self._stateView = 0;
      }
      this._templates[self._stateView].render();
    },
    renderNavigation: function () {
      var self = this;
      var source = $("#navigation-tpl").html();
      var template = Handlebars.compile(source);
      function patch(studies) {
        studies.forEach(function (research, index) {
          if (research.status === 2) {
            this[index].showSync = true;
          }
        }, studies);

        return studies;
      }
      var html = template({ studies: patch(this._studies.getAll()) });

      $("#app-navigation ul").html(html);

      // create new research
      var self = this;
      $("#new-research").click(function () {
        var conn = {};

        self._studies
          .create()
          .done(function () {
            self._stateView = 1;
            self.render();
          })
          .fail(function () {
            OC.dialogs.alert(
              t("rds", "Could not create research"),
              t("rds", "RDS Update project")
            );
          });
      });

      // show app menu
      $("#app-navigation .app-navigation-entry-utils-menu-button").click(
        function () {
          var entry = $(this).closest(".research");
          entry.find(".app-navigation-entry-menu").toggleClass("open");
        }
      );

      $("#app-navigation .research .upload").click(function () {
        self._files
          .triggerSync()
          .done(function () {
            self.render();
          })
          .fail(function () {
            OC.dialogs.alert(
              t("Could not sync research, not found"),
              t("rds", "RDS Update project")
            );
          });
      });

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
            OC.dialogs.alert(
              t("Could not delete research, not found"),
              t("rds", "RDS Update project")
            );
          });
      });

      // load a research
      $("#app-navigation .research > a").click(function () {
        var id = parseInt($(this).parent().data("id"), 10);
        self._studies.load(id);

        if (self._studies.getActive().status > 1) {
          self._files.load(self._studies.getActive().researchIndex);
        }

        self._stateView = 1;
        self.render();
      });
    },
    render: function () {
      this.renderNavigation();
      this.renderContent();
      $(".icon-info").tipsy({ gravity: "w" });
    },
    loadAll: function () {
      var self = this;

      return $.when(
        self._studies.loadAll(),
        self._services.loadAll(),
        self._studies._metadata.loadJsonSchema()
        // needed later
        //self._files.loadAll()
      );
    },
  };
})(OC, window, jQuery);
