// inspired by https://github.com/PaulLereverend/NextcloudExtract/blob/master/js/extraction.js
$(document).ready(function () {
  var addFolderToResearch = {};
  var pushFileToResearch = {
    init: function (mimetype) {
      var self = this;
      OCA.Files.fileActions.registerAction({
        name: "pdf2Zenodo",
        displayName: t("upload_zenodo", "Push this file to Zenodo"),
        mime: mimetype,
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-extract",
        actionHandler: function (filename, context) {
          /*curl -X POST -d '{"user_id": "admin", "from_service":"Owncloud", "filename":"features.txt"}' https://sciebords-│
dev.uni-muenster.de/exporter/export/Zenodo --insecure -H "Content-Type:application/json"     */
          var data = `user_id=${OC.currentUser}&from_service=Owncloud&filename=${filename}`;
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
          });
        },
      });
    },
  };

  /*
  var importZenodo = {
    attach: function(menu) {
      menu.addMenuEntry({
        id: "importZenodo",
        displayName: "Import file from zenodo",
        templateName: "templateName.ext",
        iconClass: "icon-filetype-text",
        fileType: "file",
        actionHandler: function() {
          console.log("do something here");
        }
      });
    }
  };*/

  // TODO: add checks, if the files are in a research folder
  mimes = ["text/plain", "application/pdf"];
  mimes.forEach((item) => {
    pushFileToResearch.init(item);
  });

  //TODO: check, if a folder was selected and it is not in a research folder
  //TODO: create research project in newFileMenu, if rds is activated

  //OC.Plugins.register("OCA.Files.NewFileMenu", importZenodo);
});
