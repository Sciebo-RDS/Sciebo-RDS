(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  var services;

  function reload() {
    var state = 0;
    var btns = $(".service :button");
    btns.each(function (index, elem) {
      var $this = $(this);
      $this.prop("disabled", true);

      var found = false;
      services.getAll().forEach(function (val, index) {
        if (val.servicename === $this.data("servicename")) {
          found = true;
        }
      });

      if (
        (!found || $this.attr("id") === "activateResearch") &&
        index === state
      ) {
        $this.prop("disabled", false);
      }

      if (found) {
        state += 1;
      }
    });
    // TODO: if state 0 (no buttons enabled), then show an error message: RDS currently not available
    // retest every 2 seconds, if there is RDS enabled and rerender form.
  }

  function openPopup(service) {
    var $this = $(this);
    var servicename = $this.data("servicename");

    return function () {
      var win = window.open(
        service.authorizeUrl + "&state=" + service.state,
        "_self",
        "innerWidth=1024,innerHeight=768"
      );

      var timer = setInterval(function () {
        if (win.closed) {
          clearInterval(timer);
          services.loadUser().always(function () {
            reload();
          });
        }
      }, 300);

      return false;
    };
  }

  function render() {
    var owncloud = undefined;
    var zenodo = undefined;

    services.getServices().forEach(function (service) {
      if (service.servicename === "Owncloud") {
        owncloud = service;
      }

      if (service.servicename === "Zenodo") {
        zenodo = service;
      }
    });

    if ((owncloud !== undefined) && (zenodo !== undefined)) {
      $("#activateOwncloud").click(openPopup(owncloud));
      $("#activateZenodo").click(openPopup(zenodo));
      $("#activateResearch").click(function () {
        window.location.replace(OC.generateUrl("/apps/rds?createResearch"));
      });

      return true
    }
    return false
  }

  $(document).ready(function () {
    services = new OC.rds.Services();

    $.when(services.loadService(), services.loadUser()).always(function () {
      if (render()) {
        reload();
      }
    });
  });
})(OC, window, jQuery);
