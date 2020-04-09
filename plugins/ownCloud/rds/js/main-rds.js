// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js
(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    var studies = new OC.rds.Studies(
      OC.generateUrl("/apps/rds/research"),
      new Metadata(OC.generateUrl("/apps/rds/metadata"))
    );
    var services = new OC.rds.Services(OC.generateUrl("/apps/rds/service"));
    var files = new OC.rds.Files(undefined);

    var view = new OC.rds.View(studies, services, files);
    view
      .loadAll()
      .done(function () {
        view.render();
      })
      .fail(function () {
        alert("Could not load informations");
      });
  });
})(OC, window, jQuery);
