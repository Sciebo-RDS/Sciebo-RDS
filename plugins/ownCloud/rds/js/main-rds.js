// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js
(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    var metadata = new OC.rds.Metadata();
    var studies = new OC.rds.Studies(metadata);
    var services = new OC.rds.Services();
    var files = new OC.rds.Files();

    var view = new OC.rds.View(studies, services, files);

    var params = new window.URLSearchParams(window.location.search);
    var create = false;
    if (params.has("createResearch")) {
      create = true;
      
      var newURL = location.href.split("?")[0];
      window.history.pushState('object', document.title, newURL);
    }

    view.loadAll().always(function () {
      $("#app-settings-content #btn-add-new-service").click(function () {
        window.location.href = OC.generateUrl(
          "settings/personal?sectionid=rds"
        );
      });

      if (create) {
        studies
          .create()
          .done(function () {
            view._stateView = 1;
          })
          .fail(function () {
            OC.dialogs.alert(
              t("rds", "Could not create research"),
              t("rds", "RDS Update project")
            );
          })
          .always(function () {
            view.render();
          });
      } else {
        view.render();
      }
    });
  });
})(OC, window, jQuery);
