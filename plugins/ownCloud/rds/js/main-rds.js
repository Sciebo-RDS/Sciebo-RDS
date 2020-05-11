// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js
(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    var metadata = new OC.rds.Metadata();
    var studies = new OC.rds.Studies(metadata);
    var services = new OC.rds.Services();
    var files = new OC.rds.Files();

    var view = new OC.rds.View(studies, services, files);
    view.loadAll().always(function () {
      $("#app-settings-content #btn-add-new-service").click(function () {
        window.location.href = OC.generateUrl(
          "settings/personal?sectionid=rds"
        );
      });

      var params = new window.URLSearchParams(window.location.search);
      if (params.has("createResearch")) {
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
          });
      }

      view.render();
    });
  });
})(OC, window, jQuery);
