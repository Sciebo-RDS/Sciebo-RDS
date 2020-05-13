(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  var state = 0;
  var services;

  function reload() {
    var btns = $(".service :button");
    btns.each(function (index, elem) {
      btns[index].disabled = true;
    });

    if (state === 1) {
      $("#activateOwncloud").prop("disabled", false);
    }
    if (state === 2) {
      $("#activateZenodo").prop("disabled", false);
    }
    if (state === 3) {
      $("#activateResearch").prop("disabled", false);
    }
  }

  function openPopup(service) {
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
            var found = false;

            services.getAll().forEach(function (svc) {
              if (service.servicename == svc.servicename) {
                found = true;
              }
            });

            if (found) {
              state += 1;
              reload();
            }
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

    reload();
  }

  $(document).ready(function () {
    services = new OC.rds.Services();
    reload();

    services.loadService().done(function () {
      state += 1;
      render();
      reload();
    });
  });
})(OC, window, jQuery);
