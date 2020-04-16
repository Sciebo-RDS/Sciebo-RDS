// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js
(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    var studies = new OC.rds.Studies(
      OC.generateUrl("/apps/rds/research"),
      new OC.rds.Metadata(OC.generateUrl("/apps/rds/metadata"))
    );
    var services = new OC.rds.Services(OC.generateUrl("/apps/rds/userservice"));
    var files = new OC.rds.Files(OC.generateUrl("/apps/rds/files"));

    var view = new OC.rds.View(studies, services, files);
    view
      .loadAll()
      .done(function () {
        alert("Debug: Load data successful");
      })
      .fail(function () {
        alert("Debug: Could not load informations");
      })
      .always(function () {
        view.render();
      });
  });
})(OC, window, jQuery);
