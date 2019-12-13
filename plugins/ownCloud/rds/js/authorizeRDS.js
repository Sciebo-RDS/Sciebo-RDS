(function(OC, window, $, undefined) {
  "use strict";

  $(document).ready(function() {
    function openAuthorizeOwncloud() {
      window.location.href =
        OC.generateUrl("/apps/oauth2/authorize") +
        "?response_type=code&client_id=sELuihhurmCifQV7hEyHAYSLNBedM5cBzGGnqLqU8ikg88JeNeRU69BcYMLxbNkz&redirect_uri=http://10.14.28.90/owncloud/index.php/settings/personal?sectionid=additional";
    }

    var button = document.getElementById("openAuthorizeOwncloud");
    if (button) {
      button.addEventListener("click", openAuthorizeOwncloud);
    }
  });
})(OC, window, jQuery);
