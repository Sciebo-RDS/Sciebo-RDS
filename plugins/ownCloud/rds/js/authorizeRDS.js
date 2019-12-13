(function(OC, window, $, undefined) {
  "use strict";

  $(document).ready(function() {
    function openAuthorizeOwncloud() {
      window.location.href =
        OC.generateUrl("/apps/oauth2/authorize") +
        "?response_type=code&client_id=R5c76Dyjk8wcg2NQpnbMCkRKwXW2SYSOyB1fcueqWQTfigac3oTeV24IzRT69GmF&redirect_uri=http://localhost:8080/redirect";
    }

    var button = document.getElementById("openAuthorizeOwncloud");
    if (button) {
      button.addEventListener("click", openAuthorizeOwncloud);
    }
  });
})(OC, window, jQuery);
