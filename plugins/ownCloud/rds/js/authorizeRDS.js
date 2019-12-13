(function(OC, window, $, undefined) {
  "use strict";

  $(document).ready(function() {
    function openAuthorizeOwncloud() {
      window.location.href =
        OC.generateUrl("/apps/oauth2/authorize") +
        "?response_type=code&client_id=S4MQ9MjTqb2sV47noTsQJ6REijG0u0LkScWJA2VG3LHkq7ue5t3CQPlu4ypX7RkS&redirect_uri=http://sciebords-dev.uni-muenster.de/token-service/redirect";
    }

    var button = document.getElementById("openAuthorizeOwncloud");
    if (button) {
      button.addEventListener("click", openAuthorizeOwncloud);
    }
  });
})(OC, window, jQuery);
