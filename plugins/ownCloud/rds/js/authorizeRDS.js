(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    $.ajax({
      url: OC.generateUrl("apps/rds") + "/service/Owncloud",
      success: function (result) {
        if (result.isOk == false) return;
        var state = result["state"];
        var authorize_url = result["authorizeUrl"] + "&state=" + state;

        var button = document.getElementById("openAuthorizeOwncloud");

        if (button) {
          button.addEventListener(
            "click",
            function () {
              var select = self._select;
              var win = window.open(
                OC.generateUrl("apps/rds"),
                "_self",
                "width=800,height=600,scrollbars=yes"
              );

              var timer = setInterval(function () {
                if (win.closed) {
                  clearInterval(timer);
                  location.reload();
                }
              }, 300);
            }.bind(this)
          );
        }
      },
      dataType: "json",
      async: false,
    });
  });
})(OC, window, jQuery);
