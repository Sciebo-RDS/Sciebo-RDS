// inspired by https://github.com/PaulLereverend/NextcloudExtract/blob/master/js/extraction.js
$(document).ready(function () {
  //TODO: check, if rds is activated, because all of this is only then possible.

  var addFolderToResearch = {
    init: function (mimetype) {
      var self = this;
      OCA.Files.fileActions.registerAction({
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
      OCA.Files.fileActions.registerAction({
        name: "pushFileToResearch",
        displayName: t("upload_zenodo", "Update RDS file"),
        mime: mimetype,
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-rds-research-small",
        actionHandler: function (filename, context) {
          console.log("push this file");
          // TODO push this file in the corresponding research project
          /*curl -X POST -d '{"user_id": "admin", "from_service":"Owncloud", "filename":"features.txt"}' https://sciebords-│
dev.uni-muenster.de/exporter/export/Zenodo --insecure -H "Content-Type:application/json"     */
          /*var data = `user_id=${OC.currentUser}&from_service=Owncloud&filename=${filename}`;
          console.log("send data:", data);
          $.ajax({
            type: "POST",
            async: "false",
            url: "https://sciebords-dev.uni-muenster.de/exporter/export/Zenodo",
            data: data,
            dataType: "json",
            statusCode: {
              200: function (element) {
                response = element;
                text = t("rds", "No success.");
                if (response.success) {
                  text = t("rds", `Upload ${filename} to Zenodo sucessfully.`);
                }
                OC.dialogs.alert(text, t("rds", t("rds", "Upload to Zenodo")));
              },
            },
          });*/
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

  //TODO: check, if a folder was selected and it is not in a research folder
  mimes = ["httpd/unix-directory"];
  mimes.forEach((item) => {
    addFolderToResearch.init(item);
  });
  // TODO: else: the files and folder are in a research folder, so it can be updated through rds
  pushFileToResearch.init("all");

  //TODO: create research project in newFileMenu
  OC.Plugins.register("OCA.Files.NewFileMenu", createRdsResearch);

  OCA.Files.FileActions.addAdvancedFilter(function (actions, context) {
    //TODO Add filter to actions
    // Examples:
    //https://github.com/owncloud/core/blob/d65e3c8dbd80f84f8d1cfe09ac90bfa4112b7eb3/apps/files_sharing/js/app.js#L287
    //https://github.com/owncloud/core/blob/bd3df85448af0e32bf199d6772b5b5eaf8c02091/apps/files/tests/js/fileactionsSpec.js#L696

    var fileName = context.$file.data("file");
    var mimetype = context.$file.data("mime");
    var dir = context.fileList.getCurrentDirectory();
    var rdsDirectories = JSON.parse(
      $.get(OC.generateUrl("/apps/rds/research") + "/files")
    );

    found = false;
    rdsDirectories.forEach(function (item) {
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
  });
});
