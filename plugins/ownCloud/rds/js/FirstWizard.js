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
        found = val.servicename === $this.data("servicename");
      });

      if (!found && index === state) {
        $this.prop("disabled", false);
      }

      if (found) {
        state += 1;
      }
    });
  }

  function openPopup(service) {
    var $this = $(this);
    return function () {
      var win = window.open(
        service.authorizeUrl + "&state=" + service.state,
        "oauth2-service-for-rds",
        "width=800,height=600,scrollbars=yes"
      );

      var timer = setInterval(function () {
        if (win.closed) {
          clearInterval(timer);
          services.loadUser().done(function () {
            reload();
          });
        }
      }, 300);
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

    $("#activateOwncloud").click(openPopup(owncloud));
    $("#activateZenodo").click(openPopup(zenodo));
    $("#activateResearch").click(function () {
      window.location.replace(OC.generateUrl("/apps/rds?createResearch"));
    });
  }

  $(document).ready(function () {
    services = new OC.rds.Services();

    $.when(services.loadService(), services.loadUser())
      .done(function () {
        render();
        reload();
      })
      .fail(function () {
        OC.dialogs.alert(
          t("Could not load services."),
          t("rds", "RDS Update project")
        );
      });
  });
})(OC, window, jQuery);
