(function(OC, window, $, undefined) {
  "use strict";

  $(document).ready(function() {
    function openAuthorizeOwncloud() {
      window.location.href =
        OC.generateUrl("/apps/oauth2/authorize") +
        "?response_type=code&client_id=DjuJWDG8xzXYu5ttjaKoY0KPfRKcVmhvdkt6u2Y2KZq8fFb5i2FtRiBQmBDJgAIM&redirect_uri=http://sciebords-dev.uni-muenster.de/token-service/redirect";
    }

    var button = document.getElementById("openAuthorizeOwncloud");
    if (button) {
      button.addEventListener("click", openAuthorizeOwncloud);
    }
  });
})(OC, window, jQuery);
