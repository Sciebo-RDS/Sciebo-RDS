(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  $(document).ready(function () {
    OC.rds.translations = {
      newresearch: $("#new-research-string").text(),
      saveNotFinished: $("#save-not-finished").text(),
    };
  });

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

      $("#app-content").html(html);
    },

    load: function () {
      this._beforeTemplateRenders();
      this._loadTemplate();
      this._afterTemplateRenders();
    },

    save: function () {
      return this._saveFn()
        .done(function () {})
        .fail(function () {
          alert(OC.rds.translations.saveNotFinished);
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
  OC.rds.OverviewTemplate.prototype._beforeTemplateRenders = function () {};
  OC.rds.OverviewTemplate.prototype._afterTemplateRenders = function () {};
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
    return {
      research: this._studies.getActive(),
      services: this._services.getAll(),
    };
  };
  OC.rds.ServiceTemplate.prototype._beforeTemplateRenders = function () {};
  OC.rds.ServiceTemplate.prototype._afterTemplateRenders = function () {
    var self = this;

    $("#app-content #btn-save-research").click(function () {
      self.save();
    });

    $("#app-content #btn-save-research-and-continue").click(function () {
      self.save_next();
    });
  };
  OC.rds.ServiceTemplate.prototype._saveFn = function () {
    var self = this;
    var portIn = [];
    var portOut = [];

    self._services.getAll().forEach(function (element) {
      var properties = [];
      var tempPortIn = {};
      var tempPortOut = {};

      var value = $(
        "input[name='radiobutton-" + element.servicename + "']:checked"
      ).val();

      tempPortIn["port"] = element.servicename;
      tempPortOut["port"] = element.servicename;

      var propertyProjectInService = {
        key: "projectId",
        value: value,
      };
      properties.push({
        portType: "customProperties",
        value: [propertyProjectInService],
      });

      $.each(
        $(
          "input[name='checkbox-" + element.servicename + "-property']:checked"
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

    return self._studies.updateActive(portIn, portOut);
  };

  OC.rds.MetadataTemplate = function (divName, view, studies) {
    OC.rds.AbstractTemplate.call(this, divName, view);

    this._studies = studies;
  };

  OC.rds.MetadataTemplate.prototype = Object.create(
    OC.rds.AbstractTemplate.prototype,
    {
      constructor: OC.rds.MetadataTemplate,
    }
  );
  OC.rds.MetadataTemplate.prototype._beforeTemplateRenders = function () {};
  OC.rds.MetadataTemplate.prototype._afterTemplateRenders = function () {
    console.log(this._studies._metadata.getSchema());
    $("#metadata-jsonschema-editor").alpaca({
      schema: this._studies._metadata.getSchema(),
    });
  };
  OC.rds.MetadataTemplate.prototype._getParams = function () {};
  OC.rds.MetadataTemplate.prototype._saveFn = function () {
    return $.when();
  };

  OC.rds.FileTemplate = function (divName, view, services, studies) {
    OC.rds.AbstractTemplate.call(this, divName, view);
  };
  OC.rds.FileTemplate.prototype = Object.create(
    OC.rds.AbstractTemplate.prototype,
    {
      constructor: OC.rds.FileTemplate,
    }
  );

  OC.rds.FileTemplate.prototype._beforeTemplateRenders = function () {};
  OC.rds.FileTemplate.prototype._afterTemplateRenders = function () {};
  OC.rds.FileTemplate.prototype._getParams = function () {};
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
        this._studies
      ),
      new OC.rds.FileTemplate(
        "#research-edit-file-tpl",
        this,
        this._services,
        this._studies
      ),
    ];
  };

  OC.rds.View.prototype = {
    renderContent: function () {
      var self = this;
      this._templates[self._stateView].load();
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
        self._stateView = 1;
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
        self._services.loadAll(),
        self._studies._metadata.loadJsonSchema()
        // needed later
        //self._files.loadAll()
      );
    },
  };
})(OC, window, jQuery);
