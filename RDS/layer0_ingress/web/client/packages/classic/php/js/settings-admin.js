$(document).ready(function () {

	$('#rds_submit').on('click', function (event) {
		event.preventDefault();
		OC.msg.startSaving('#rdsSettings .msg');

		var app = "rds"
		var url = $("#cloud_url");
		var urlValue = url.val();
		if (urlValue.endsWith("/")) {
			urlValue = urlValue.slice(0, -1);
			url.val(urlValue);
		}
		OC.AppConfig.setValue(app, url.attr('name'), url.val());

		var oauthname = $("#oauth_name");
		OC.AppConfig.setValue(app, oauthname.attr('name'), oauthname.val());

		OC.msg.finishedSaving('#rdsSettings .msg', { status: 'success', data: { message: t('rds', 'Saved.') } });
	});

	$('.section .icon-info').tipsy({ gravity: 'w' });
});

