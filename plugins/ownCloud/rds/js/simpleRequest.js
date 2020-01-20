// inspired by https://github.com/PaulLereverend/NextcloudExtract/blob/master/js/extraction.js
$(document).ready(function() {
  var actionsSimple = {
    init: function() {
      var self = this;
      OCA.Files.fileActions.registerAction({
        name: "reverseText",
        displayName: t("export_zenodo", "Export to Zenodo"),
        mime: "text",
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-extract",
        actionHandler: function(filename, context) {
          /*var data = {
            text: filename
          };

          getReversedText(data);*/
          console.log("do something here");
        }
      });
    }
  };

  var pdfSimple = {
    init: function() {
      var self = this;
      OCA.Files.fileActions.registerAction({
        name: "pdf2Word",
        displayName: t("make_word", "Convert to Word"),
        mime: "application/pdf",
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-extract",
        actionHandler: function(filename, context) {
          /*var data = {
            text: filename
          };

          getReversedText(data);*/
          console.log("do something here");
        }
      });
    }
  };
  

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
  };

  function getReversedText(request) {
    $.ajax({
      type: "POST",
      async: "false",
      url: "http://sciebords-dev.uni-muenster.de/api/time/text/reverse",
      data: JSON.stringify(request),
      statusCode: {
        200: function(element) {
          response = element;
          OC.dialogs.alert(
            t("reverse", response.myReversedText),
            t("reverse", "reversed " + request.text)
          );
        },
        201: function() {
          getReversedText(request);
        },
        202: function() {
          getReversedText(request);
        }
      }
    });
  }

  actionsSimple.init();
  pdfSimple.init();
  OC.Plugins.register('OCA.Files.NewFileMenu', importZenodo);
});
