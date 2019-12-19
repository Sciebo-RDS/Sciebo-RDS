(function(OC, window, $, undefined) {
  "use strict";

  $(document).ready(function() {
    $.ajax({
      url: OC.generateUrl("apps/rds/api/v1") + "/service/Owncloud",
      success: function(result) {
        if (result.isOk == false) return;
        var state = result["state"];
        var authorize_url = result["authorize_url"] + "&state=" + state;

        var button = document.getElementById("openAuthorizeOwncloud");

        if (button) {
          button.addEventListener(
            "click",
            function() {
              window.location.href = authorize_url;
            }.bind(this)
          );
        }
      },
      dataType: "json",
      async: false
    });
  });
})(OC, window, jQuery);
