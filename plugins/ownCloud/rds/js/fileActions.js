// inspired by https://github.com/PaulLereverend/NextcloudExtract/blob/master/js/extraction.js
(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  var fileActions = OCA.Files.fileActions;

  var addFolderToResearch = {
    init: function (mimetype) {
      var self = this;
      fileActions.registerAction({
        name: "addFolderToResearch",
        displayName: t("upload_zenodo", "Add folder to RDS"),
        mime: mimetype,
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-rds-research-small",
        actionHandler: function (filename, context) {
          //TODO: implement here the stuff
          console.log("add here the folder to a research project");
        },
      });
    },
  };

  var pushFileToResearch = {
    init: function (mimetype) {
      var self = this;
      fileActions.registerAction({
        name: "pushFileToResearch",
        displayName: t("upload_zenodo", "Update RDS file"),
        mime: mimetype,
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-rds-research-small",
        actionHandler: function (filename, context) {
          var data = {
            filename: filename,
          };

          $.ajax({
            type: "POST",
            url: OC.generateUrl("/apps/rds/research/files"),
            data: JSON.stringify(data),
            dataType: "json",
          })
            .done(function () {
              OC.dialogs.alert(
                t(
                  "rds",
                  "File was successfully uploaded to outgoing services."
                ),
                t("rds", "RDS upload directly through Files app")
              );
            })
            .fail(function () {
              OC.dialogs.alert(
                t("rds", "File upload to outgoing services failed."),
                t("rds", "RDS upload directly through Files app")
              );
            });
        },
      });
    },
  };

  var createRdsResearch = {
    attach: function (menu) {
      menu.addMenuEntry({
        id: "createRdsResearch",
        displayName: "RDS research project",
        templateName: "templateName.ext",
        iconClass: "icon-rds-research-small",
        fileType: "file",
        actionHandler: function () {
          console.log("go to rds and create a research project");
        },
      });
    },
  };

  OC.Plugins.register("OCA.Files.NewFileMenu", createRdsResearch);

  OC.rds.ResearchDirectories = function () {
    this._folders = [];
  };

  OC.rds.ResearchDirectories.prototype = {
    getFolders: function () {
      return this._folders;
    },
    load: function () {
      var self = this;
      var deferred = $.Deferred();
      $.get(OC.generateUrl("/apps/rds/research") + "/files")
        .done(function (directories) {
          self._folders = directories;
          deferred.resolve();
        })
        .fail(function () {
          deferred.reject();
        });
      return deferred.promise();
    },
  };

  var directories = new OC.rds.ResearchDirectories();
  var activate = true;
  directories.load().fail(function () {
    console.log(
      "cannot find directories. Could be possible, that rds is not activated?"
    );
    activate = false;
  });

  if (activate) {
    fileActions.addAdvancedFilter(function (actions, context) {
      var fileName = context.$file.data("file");
      var mimetype = context.$file.data("mime");
      var dir = context.fileList.getCurrentDirectory();

      found = false;
      directories.getFolders().forEach(function (item) {
        if (item === dir) {
          found = true;
        }
      });

      if (found) {
        if (mimetype === "httpd/unix-directory") {
          delete actions.addFolderToResearch;
        }
      } else {
        delete actions.pushFileToResearch;
      }

      return actions;
    });

    var mimes = ["httpd/unix-directory"];
    mimes.forEach((item) => {
      addFolderToResearch.init(item);
    });
    pushFileToResearch.init("all");
  }
})(OC, window, jQuery);
