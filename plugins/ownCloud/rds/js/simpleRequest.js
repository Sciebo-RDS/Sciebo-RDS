// inspired by https://github.com/PaulLereverend/NextcloudExtract/blob/master/js/extraction.js
$(document).ready(function() {
  var actionsSimple = {
    init: function() {
      var self = this;
      OCA.Files.fileActions.registerAction({
        name: "reverseText",
        displayName: t("reverse", "Reverse text"),
        mime: "text",
        permissions: OC.PERMISSION_UPDATE,
        type: OCA.Files.FileActions.TYPE_DROPDOWN,
        iconClass: "icon-extract",
        actionHandler: function(filename, context) {
          var data = {
            text: filename
          };

          getReversedText(data);
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
          getReversedText(request)
        },
        202: function() {
          getReversedText(request)
        }
      }
    });
  }

  actionsSimple.init();
});
