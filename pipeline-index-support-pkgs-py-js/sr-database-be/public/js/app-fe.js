/*
    Author: Shankar K (Oct 2019)
    Description:
        simple front end enhancing handlebars
*/

function stat_plt(s, e) {
    var phash = {};
    var ch = $("#srlist").children()
    ch.each((i, v) => {
        var sr = v.cells[0].textContent;
        var p = v.cells[3].textContent;
        var d = new Date(v.cells[2].textContent)
        if ((d < s) || (d > e)) {
            return;
        }
        if (!p) {
            return;
        }
        var pn = p.match(/Platform: (.*?);/m);
        pn = pn || p.match(/Product Name: (.*?);/m)
        var plt = 'Unknown';
        if (pn) {
            plt = pn[1].replace(/NetScaler Virtual Appliance NSSDX/g, 'NSSDX');
            plt = plt.replace(/(NSSDX.*) 45\d+$/, '$1')
            plt = plt.replace(/(NSMPX.*?) .*/, '$1')
            if (plt.match(/SDX|MPX/))
                plt = plt.replace(/ /g, '-');
        }
        var val = phash[plt] || 0
        phash[plt] = val + 1
    })
    var htmlstr = '';
    var keys = Object.keys(phash)
    keys.sort(function (a, b) {
        return phash[b] - phash[a];
    });
    htmlstr = '<div class="table-responsive col-md-6"><table class="table table-striped table-bordered">'
    keys.forEach(function (k) {
        var adm = ''
        for (p in phglobal) {
            var re = new RegExp(p, 'g');
            if (k.match(re)) {
                adm = ' (' + phglobal[p] + ')';
                break;
            }
        }
        htmlstr += '<tr>' + '<td>' + k + adm + '</td>' + '<td>' + phash[k]
        '</td>' + '</tr>'
    })
    htmlstr += '</table></div>'
    return htmlstr;
}

function stat_bld(s, e) {
    var phash = {};
    var ch = $("#srlist").children()
    ch.each((i, v) => {
        var sr = v.cells[0].textContent;
        var p = v.cells[3].textContent;
        var d = new Date(v.cells[2].textContent)
            //console.log(d + ' : ' + s + "-" + e);
        if ((d < s) || (d > e)) {
            return;
        }
        if (!p) {
            return;
        }
        var getNS = function (f1, f2, f3) {
            var val = phash[f2] || 0
            phash[f2] = val + 1
        };
        var getSBI = function (f1, f2, f3) {
            var val = phash['SBI' + f2] || 0
            phash['SBI' + f2] = val + 1
        };
        var getSVM = function (f1, f2, f3) {
            var val = phash['SVM' + f2] || 0
            phash['SVM' + f2] = val + 1
        };
        p.replace(/NetScaler (NS.*?): /g, getNS)
        p.replace(/SDX_PLATFORM_SBI=(.*?)-/g, getSBI)
        p.replace(/svm-(.*?)-/g, getSVM)
    })
    var htmlstr = '';
    var keys = Object.keys(phash)
    keys.sort(function (a, b) {
        return phash[b] - phash[a];
    });
    htmlstr = '<div class="table-responsive col-md-6"><table class="table table-striped table-bordered">'
    keys.forEach(function (k) {
        htmlstr += '<tr>' + '<td>' + k + '</td>' + '<td>' + phash[k] + '</td>' + '</tr>'
    })

    htmlstr += '</table></div>'
    return htmlstr;
}

var phglobal = {
    '450000': 'XEN',
    '450001': 'XEN_CISCO',
    '450010': 'ESX',
    '450011': 'ESX_CISCO',
    '450020': 'HYP',
    '450021': 'HYP_CISCO',
    '450070': 'KVM',
    '450071': 'KVM_CISCO',
    '450040': 'AWS',
    '450090': 'CPX',
    '450091': 'BLX',
};


$(document).ready(function () {
    $("#Stat").click(function (e) {
        var locn = window.location.pathname;
        window.location.hash = "#stats"
        var s = $("#FD").val() || null;
        var e = $("#LD").val() || Date.now();
        s = new Date(s);
        e = new Date(e);
        var plthtml = stat_plt(s, e);
        var bldhtml = stat_bld(s, e);
        $("#stats").html('<div class="row">' + plthtml + bldhtml + '</div')
        this.style.display= "none";
        $("#stat_date")[0].style.display = "none";
    });
    $(function () {
        $(".datepicker").datepicker({
            changeMonth: true,
            changeYear: true,
            changeDate: true,
            showButtonPanel: true,
            dateFormat: 'yy-mm-dd',
            onClose: function (dateText, inst) {
                $(this).datepicker();
            }
        });
    });

});
