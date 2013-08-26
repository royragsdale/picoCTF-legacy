var tabsLI = [
    ['compete', 'Game'],
    ['irc', 'chat'],
    ['webshell', 'Shell'],
    ['scoreboard', 'Scoreboard'],
    ['news', 'News'],
    ['learn', 'Learn'],
    ['faq', 'FAQ'],
    ['account', 'Account'],
    ['logout', 'Logout']
];
var tabsNLI = [
    ['about', 'About'],
    ['scoreboard', 'Scoreboard'],
    ['faq', 'FAQ'],
    ['registration', 'Registration'],
    ['news', 'News'],
    ['learn', 'Learn'],
    ['contact', 'Contact'],
    ['login', 'Login']
];
var tabsFail = [
    ['about', 'About'],
    ['faq', 'FAQ'],
    ['learn', 'Learn'],
    ['contact', 'Contact']
];

function show_site_down_error() {
	$(".contentbox").html('<div class="row-fluid"><div class="offset1 span10"><div class="alert"><button type="button" class="close" data-dismiss="alert">&times;</button>An error occured. picoCTF may be down. Please contact use at <a href="mailto:support@picoctf.com">support@picoctf.com</a></div></div></div>');
}

function build_navbar(tabs) {
    var ohtml = "";
    for (var i = 0; i < tabs.length; i++) {
        if (window.location.href.indexOf(tabs[i][0]) != -1) {
            ohtml += '<li class="ts_selected" id="ts_' + tabs[i][0] + '"><a href="' + tabs[i][0] + '">' + tabs[i][1] + '</a></li>';
        } else {
            ohtml += '<li id="ts_' + tabs[i][0] + '"><a href="' + tabs[i][0] + '">' + tabs[i][1] + '</a></li>';
        }
    }
    $("#navbar")[0].innerHTML = ohtml;
}

function add_certs_link() {
    var ohtml = $("#navbar")[0].innerHTML;
    if (window.location.href.indexOf("certificates") != -1) {
        ohtml = '<li class="ts_selected" id="ts_certificates"><a href="certificates">Certificates</a></li>' + ohtml;
    } else {
        ohtml = '<li id="ts_certificates"><a href="certificates">Certificates</a></li>' + ohtml;
    }
    $("#navbar")[0].innerHTML = ohtml;
}

function check_certs_link_necessary() {
    if (typeof(Storage) != "undefined") {
        if (sessionStorage.showCertsLink == "true")
            add_certs_link();
        else {
            $.ajax({
                type: "GET",
                url: "/api/getlevelcompleted",
                cache: false
            }).done(function (data) {
                    if (data['success'] == 1 && data['level'] > 0) {
                        sessionStorage.showCertsLink = "true";
                        add_certs_link();
                    }
                    else
                        sessionStorage.showCertsLink = "false";
                }).fail(function(data) {
                    sessionStorage.showCertsLink = "false";
                });
        }
    }
    else
        $.ajax({
            type: "GET",
            url: "/api/getlevelcompleted",
            cache: false
        }).done(function (data) {
                if (data['success'] == 1 && data['level'] > 0)
                    add_certs_link();
            });
}

function display_navbar() {
    if (typeof(Storage) != "undefined") {
        if (sessionStorage.signInStatus == "loggedIn") {
            build_navbar(tabsLI);
            check_certs_link_necessary();
        }
        else if (sessionStorage.signInStatus == "notLoggedIn")
            build_navbar(tabsNLI);
        else if (sessionStorage.signInStatus == "apiFail")
            build_navbar(tabsFail);
        else
            build_navbar(tabsNLI);
        $.ajax({
            type: "GET",
            url: "/api/isloggedin",
            cache: false
        }).done(function (data) {
                if (data['success'] == 1 && sessionStorage.signInStatus != "loggedIn") {
                    sessionStorage.signInStatus = "loggedIn";
                    build_navbar(tabsLI);
                    check_certs_link_necessary();
                }
                else if (data['success'] == 0 && sessionStorage.signInStatus != "notLoggedIn") {
                    sessionStorage.signInStatus = "notLoggedIn";
                    build_navbar(tabsNLI);
                }
            }).fail(function () {
                if (sessionStorage.signInStatus != "apiFail") {
                    sessionStorage.signInStatus = "apiFail";
                    build_navbar(tabsFail);
                    show_site_down_error();
                }
            });
    }
    else
        $.ajax({
            type: "GET",
            url: "/api/isloggedin",
            cache: false
        }).done(function (data) {
                build_navbar(data['success'] == 1 ? tabsLI : tabsNLI);
            }).fail(function () {
                build_navbar(tabsFail);
                show_site_down_error();
            });
}

function load_footer() {
    $.ajax({
        type: "GET",
        cache: false,
        url: "deps/footer.html"
    }).done(function (data) {
            $("#footer").html(data);
        });
}

function handle_submit(prob_id) {
    $.ajax({
        type: "POST",
        cache: false,
        url: "/api/submit",
        dataType: "json",
        data: {
            'pid': prob_id,
            'key': $("#" + prob_id).val()
        }
    }).done(function (data) {
            var prob_msg = $("#msg_" + prob_id);
            var alert_class = "";
            if (data['status'] == 0){
                alert_class = "alert-error";
            }
            else if (data['status'] == 1){
                alert_class = "alert-success";
            }
            prob_msg.hide().html('<div class="alert ' + alert_class + '">' + data['message'] + '</div>').slideDown('normal');
            setTimeout(function () {
                prob_msg.slideUp('normal', function () {
                    prob_msg.html('').show();
                    if (data['status'] == 1)
                        window.location.reload();
                })
            }, 2500);
        });
}

function redirect_if_not_logged_in() {
    $.ajax({
        type: "GET",
        url: "/api/isloggedin",
        cache: false
    }).done(function (data) {
            if (data['success'] == 0)
                window.location.href = '/login';
        }).fail(function () {
            window.location.href = '/';
        });
}
