// inspired by https://github.com/PaulLereverend/NextcloudExtract/blob/master/js/extraction.js
$(document).ready(function() {
  var pdfZenodo = {
    init: function() {
      var self = this;
      OCA.Files.fileActions.registerAction({
        name: "pdf2Zenodo",
        displayName: t("upload_zenodo", "Push this file to Zenodo"),
        mime: "application/pdf",
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-extract",
        actionHandler: function(filename, context) {
          /*curl -X POST -d '{"user_id": "admin", "from_service":"Owncloud", "filename":"features.txt"}' https://sciebords-│
dev.uni-muenster.de/exporter/export/Zenodo --insecure -H "Content-Type:application/json"     */
          var data = {
            user_id: OC.currentUser,
            from_service: "Owncloud",
            filename: filename
          };
          console.log("send data:", data);
          $.ajax({
            type: "POST",
            async: "false",
            url: "https://sciebords-dev.uni-muenster.de/exporter/export/Zenodo",
            data: JSON.stringify(data),
            dataType: "json",
            statusCode: {
              200: function(element) {
                response = element;
                if (response.success == "True") {
                  text = "Upload " + filename + " to Zenodo sucessfully.";
                } else {
                  text = response;
                }

                OC.dialogs.alert(t("rds", text));
              }
            }
          });
        }
      });
    }
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
  
  pdfZenodo.init();
  //OC.Plugins.register("OCA.Files.NewFileMenu", importZenodo);
});
