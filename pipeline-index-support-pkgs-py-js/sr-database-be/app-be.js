const express = require('express'),
    app = express();
const exphbs = require('express-handlebars')
const bodyParser = require('body-parser');
const path = require('path');
const mongoose = require('mongoose');
const J = require('jira-client');
const Schema = mongoose.Schema;

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/sr-db', {
    useNewUrlParser: true,
    useCreateIndex: true
});

const srSchema = new Schema({
    sr: String,
    lat: {
        type: String,
    },
    lmt: {
        type: String,
    },
    pkg: {
        type: Array,
    },
    date: {
        type: Date,
        default: Date.now,
    },
    dirty: {
        type: Boolean,
        default: false,
    },
    bld: {
        type: String,
    },
    plt: {
        type: String,
    },
    jiraid: {
        type: String,
    },
    cname: {
        type: String,
    },
    files: {}, // raw data
    P: {}, // processed data
});
srSchema.index({
    lmt: -1
}, {
    "background": false
})
const srdb = mongoose.model('srmodel', srSchema);

app.engine('handlebars', exphbs({
    defaultLayout: 'main'
}));
app.set('view engine', 'handlebars');
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json({
    parameterLimit: 100000,
    limit: '50mb',
    extended: true
}));
app.use(express.static(path.join(__dirname, '/public')));

var port = process.env.PORT || 2567;
var lut;

app.route('/').get(home);
app.route('/lut').post(lutime);
app.route('/lut').get(lutime);
app.route('/list').get(list_sr);
app.route('/filter').post(filter_sr);
app.route('/check').post(check_sr);
app.route('/:sr').post(save_sr);
app.route('/:sr').get(get_sr);
app.listen(port);

// policy:
// -------
// investigate how to monitor agent.conf and set dirty bit

function processdata(x) {
    var fl = x['files']
    x['P'] = {}
    var d = x['P']
    for (f in fl) {
        var m; //console.log(f)
        if ((m = f.match(/(Management.*?)\//))) {
            var svm = m[1];
            if (!(svm in d)) d[svm] = '';
            if (f.match(/dmesg/)) {
                m = fl[f].match(/platform: sys(.*?)\n/g)
                for (i in m.sort()) d[svm] += m[i];
                m = fl[f].match(/\/flash\/.*\d+.*\n/g)
                d[svm] += 'Build: ' + m
                m = fl[f].match(/freebsd.*netscaler.*/ig)
                d[svm] += m
            }
        } else if ((m = f.match(/(collector.*?)\//))) {
            var ns = m[1]
            if (!(ns in d)) d[ns] = '';
            if (f.match(/showcmds/)) {
                m = fl[f].match(/show ns hardware\n\t(.*?)\n/)
                if (m) {
                    var nsplt = m[1] + '\n'
                    m = fl[f].match(/show ns version\n\t(.*?)\n/)
                    if (m) {
                        d[ns] = nsplt + m[1] // note '=' not '+='
                    }
                }
            }
            if (d[ns].length == 0 && f.match(/dmesg/)) {
                m = fl[f].match(/platform: (.*?)\n/g)
                for (i in m.sort()) d[ns] += m[i];
                m = fl[f].match(/netscaler.version=(.*?)\n/)
                if (m) d[ns] += 'Build: ' + m[1];
                else d[ns] += 'netscaler.version not found';
            }
        } else if ((m = f.match(/(bug-report.*?)\//))) {
            var xen = m[1]
            if (!(xen in d)) d[xen] = '';
            if (f.match(/dmidecode/)) {
                m = fl[f].match(/(Product Name: [^]+)UUID/)
                if (m) d[xen] += m[1];
            }
            if (f.match(/inventoryxml/)) {
                m = fl[f].match(/(uname=.*?) (uptime=.*?)\n/)
                if (m) d[xen] += m[1] + '\n' + m[2].replace(/,.*/, '') + '\n'
            }
            if (f.match(/xensource-inventory/)) {
                m = fl[f].match(/PRODUCT_VERSION=.*?\n/g)
                if (m) d[xen] += m
                m = fl[f].match(/INSTALLATION_DATE=.*?\n/g)
                if (m) d[xen] += m
            }
            if (f.match(/xapi-dbxml/)) {
                m = fl[f].match(/software_version=\".*?\" /g)
                if (m) d[xen] += m[0].replace(/\)\s+\(/g, ';')
            }
            if (f.match(/sdx-inventory/)) {
                m = fl[f].match(/SDX_PLATFORM=.*?\n/g)
                if (m) d[xen] += '\n' + m
                m = fl[f].match(/SDX_PLATFORM_SBI=.*?\n/g)
                if (m) d[xen] += '\n' + m
            }
        } else {
            console.log('Unknown ' + f);
        }
    }
}

function updatejira(d, srdb) {
    var j = new J({
        protocol: 'https',
        host: 'issues.citrite.net',
        username: 'svcacct_jira_odsbo',
        password: '9qFx%3oJ(S*$f38o'
    });
    var qstr = "project=NSHELP AND cf[20330] ~ " + d.sr
    var qopt = {
        maxResults: 10,
        fields: ['key', 'customfield_13930', 'customfield_20330'],
    };
    j.searchJira(qstr, qopt)
        .then((idl) => {
            d.jiraid = ''
            d.cname = ''
            for (i in idl.issues) {
                d.jiraid += ((i == 0) ? '' : ',') + idl.issues[i].key
                d.cname += ((i == 0) ? '' : ',') + idl.issues[i].fields.customfield_13930
            }
            //console.log(idl);
            srdb.updateOne({
                sr: d.sr
            }, {
                jiraid: d.jiraid,
                cname: d.cname
            }, {
                upsert: true
            }, (err, d) => {
                if (err) console.log('Err: ' + err);
            })
        })
}

function dateformat(m) {
    if (m)
        return new Date(m * 1000).toISOString().
    replace(/T/, ' ').replace(/\..+/, '');
    else
        return 'null';
}

function lutime(req, res) {
    lut = Date.now() / 1000;
    //console.log(lut);
    res.send({
        res: 'ok'
    })
}

function combine(s1, s2) {
    var spat = '<b>.*?</b>'
    var vpat = '<i>.*?</i>'
    var re = new RegExp(spat, 'g')
    var re1 = new RegExp(vpat, 'g')
    var h = {}
    s1 = s1.replace(/\n/g, "")
    s2 = s2.replace(/\n/g, "")
    var k = s1.match(re)
    var v = s1.match(re1)
    for (var i in k) {
        h[k[i]] = v[i]
    }
    k = s2.match(re)
    v = s2.match(re1)
    for (var i in k) {
        if (k[i] in h) {
            h[k[i]] += ';' + v[i]
        } else {
            h[k[i]] = v[i]
        }
    }
    return Object.entries(h).join(',')
}

function pkglist(m) {
    var pkgstr = '';
    m.forEach((i) => {
        pkgstr += i + '<br>';
    })
    return pkgstr;
}

function bldlist(p) {
    var bldlist = '';
    for (var k in p) {
        if (m = k.match(/bug-report/)) {
            var tt = p[k].replace(/['"]/g, '').replace(/\n/, '<br>');
            var tv = '';
            var m = p[k].match(/SDX_PLATFORM_SBI=.*/)
            if (m) tv = m[0];
            else tv = 'Legacy Build';
            tt = '<span data-toggle="tooltip" data-html="true" title="' + tt + '">' + tv + '</span>'
            bldlist += '<b>' + k + ':</b>' + '<i>' + tt + '</i>';
        } else {
            var m = p[k].match(/\n.*build.*/i);
            if (m) {
                var cont = m[0].replace(/\/flash\//, '').replace(/, Date.*/, '')
                bldlist += '<b>' + k + ':</b> ' + '<i>' + cont + '</i>' + '<br>';
            }
        }
    }
    return bldlist;
}

function pltlist(p) {
    var pltlist = '';
    for (var k in p) {
        if (m = k.match(/bug-report/)) {
            var tt = p[k].replace(/['"]/g, '').replace(/\n/, '<br>');
            var tv = '';
            var m = p[k].match(/product name.*/i)
            if (m) tv = m[0]
            else tv = "dmidecode missing (hover here)"
            tt = '<span data-toggle="tooltip" data-html="true" title="' + tt + '">' + tv + '</span>'
            pltlist += '<b>' + k + ':</b>' + '<i>' + tt + '</i>';
        } else {
            var m = p[k].match(/.*\n/);
            if (m)
                pltlist += '<b>' + k + ':</b> ' + '<i>' + m[0] + '</i>' + '<br>';
        }
    }
    return pltlist;
}

function annosr(m) {
    return '<a href=\"/' + m + "\">" + m + '</a>';
}

function index(req, res, srl) {
    var q = req.query;
    var s = 0,
        e = 10;

    if (q && 'id' in q) {
        [s, e] = q['id'].split('-');
        s = parseInt(s);
        e = parseInt(e);
        if (!(0 <= s < srl.length && 0 <= e < srl.length && s <= e)) {
            s = 0;
            e = 10
        }
    }
    var srlist = []; //console.log(' s '+s + ' e '+ e);
    for (var i = s; i < e; i++) {
        var sre = srl[i];
        var bld = bldlist(sre['P'])
        var plt = pltlist(sre['P'])
        var tmp = {}
        tmp = {
            sr: annosr(sre['sr']),
            lmt: dateformat(sre['lmt']),
            pkg: pkglist(sre['pkg']),
            bld: bld,
            plt: plt,
            bp: combine(plt, bld),
            jid: sre['jiraid'],
            cn: sre['cname'],
        };
        srlist.push(tmp)
    }
    //var srlist = srl.splice(s,e);
    render_srl(req, res, srlist, srl.length, s, e, 'index')
}

function render_srl(req, res, srs, n, s, e, ty) {

    var pe = s,
        ns = e;
    var ps = pe - 10,
        ne = ns + 10;
    if (ps < 0) {
        ps = 0;
        pe = 10
    }
    if (ne > n) {
        ne = n;
        ns = Math.max(0, n - 1)
    }
    res.render(ty, {
        plt: ["PLATFORM TYPE", "SDX", "MPX", "VPX", "VPX (NON-SDX)", "MISC"],
        bld: ["MR BUILD", "10.1", "10.5", "11.0", "11.1", "12.0", "12.1", "13.0"],
        srlist: srs,
        total: n,
        lut: dateformat(lut),
        s: s,
        e: e,
        pe: pe,
        ns: ns,
        ne: ne,
        ps: ps,
        fpage: (ty == 'filter'),
    });
}

function isEmpty(obj) {
    return !Object.keys(obj).length;
    //return false;
}

function filter(req, res, srl) {
    var b = req.body
    var validplt = ["SDX", "MPX", "VPX", "VPX (NON-SDX)", "MISC", "Virtual"];
    var validbld = ["10.1", "10.5", "11.0", "11.1", "12.0", "12.1", "13.0"];
    if (!(validplt.includes(b["TYPE"]) ||
            validbld.includes(b["MR"])) && !('JIRA' in b)) {
        res.redirect('/');
        return
    }

    if ('JIRA' in b) {
        for (var i = srl.length - 1; i >= 0; i--) {
            if (!('jiraid' in srl[i] && srl[i]['jiraid'].length > 0)) {
                srl.splice(i, 1);
            }
        }
    }

    var sri = []
    if (validplt.includes(b["TYPE"])) {
        var srchpat = b['TYPE']
        var nonsdx = (srchpat.includes('NON-SDX')) ? true : false;
        if (b['TYPE'].includes('VPX')) srchpat = 'Virtual';
        var re = new RegExp(srchpat, 'g');
        for (var i = 0; i < srl.length; i++) {
            var plt = pltlist(srl[i]['P']);
            var f = false;
            if (b['TYPE'] == 'MISC') {
                if (!isEmpty(srl[i]['P']) && !(plt.match(/SDX|MPX|Virtual/)))
                    f = true;
            } else {
                if (plt.match(re)) {
                    if (!(nonsdx && plt.match('SDX')))
                        f = true;
                }
            }
            if (!f) continue;
            sri.push(i);
        }
    }
    //console.log(' plt len ' + sri.length);
    if (validbld.includes(b["MR"])) {
        var pat = 'NS' + b['MR'];
        pat += '|' + 'svm-' + b['MR']
        pat += '|' + 'SBI=' + b['MR']
        var re = new RegExp(pat, 'g')
        if (validplt.includes(b["TYPE"])) {
            for (var i = sri.length - 1; i >= 0; i--) {
                var bld = bldlist(srl[sri[i]]['P']);
                if (!bld.match(re)) sri.splice(i, 1);
                //else console.log('sr ' + srl[sri[i]]['sr'] + ' ' + bld + ' matching ' + b['MR'])
            }
        } else {
            for (var i = 0; i < srl.length; i++) {
                var bld = bldlist(srl[i]['P']);
                if (bld.match(re)) sri.push(i);
            }
        }
    }
    if (!(validplt.includes(b["TYPE"]) ||
            validbld.includes(b["MR"]))) {
        sri = Array.from(Array(srl.length).keys())
    }

    var srfl = []
    for (var i = 0; i < sri.length; i++) {
        var sre = srl[sri[i]];
        var bld = bldlist(sre['P'])
        var plt = pltlist(sre['P'])
        var tmp = {
            sr: annosr(sre['sr']),
            lmt: dateformat(sre['lmt']),
            pkg: pkglist(sre['pkg']),
            bld: bld,
            plt: plt,
            bp: combine(plt, bld),
            jid: sre['jiraid'],
            cn: sre['cname'],
        };
        srfl.push(tmp);
    }
    var n = srfl.length;
    render_srl(req, res, srfl, n, 0, n, 'filter')
}

function filter_sr(req, res) {
    //console.log('body ' + JSON.stringify(req.body));
    var b = req.body;
    if (!('TYPE' in b && 'MR' in b && 'SR' in b))
        res.redirect('/');
    if ('SR' in b && b['SR'].length > 0) {
        res.redirect('/' + b['SR'])
    } else {
        srdb.find({}, {
                sr: 1,
                P: 1,
                pkg: 1,
                lmt: 1,
                jiraid: 1,
                cname: 1,
            }, {
                lean: true
            })
            .sort({
                lmt: 'desc'
            }) // 'asc'
            .then((srl) => filter(req, res, srl))
            .catch((err) => res.send(err));
    }
}

function list_sr(req, res) {
    srdb.find({}, {
            sr: 1,
            P: 1,
            pkg: 1,
            lmt: 1,
            jiraid: 1,
            cname: 1,
        }, {
            lean: true
        })
        .sort({
            lmt: 'desc'
        }) // 'asc'
        .then((srl) => index(req, res, srl))
        .catch((err) => res.send(err));
}

function home(req, res) {
    res.redirect('/list');
}

function get_sr(req, res) {
    srdb.findOne({
            sr: req.params.sr
        }, '-name', {
            lean: true
        })
        .then((d) => {
            if (req.query['full'] == 0) delete d['files'];
            res.send(d);
        })
        .catch((err) => res.send(err));
}

function save_sr(req, res) {
    var fl = {}
    for (i in req.body['FILES']) {
        var j = i.replace(/\./g, '');
        fl[j] = req.body['FILES'][i]
    }
    var data = {
        sr: req.params.sr,
        lat: req.body['LAT'],
        pkg: req.body['PKG'],
        lmt: req.body['LMT'],
        files: fl,
    };
    data.date = new Date(Date.now())
    processdata(data)
    updatejira(data, srdb)
    srdb.updateOne({
        sr: req.params.sr
    }, data, {
        upsert: true
    }, (err, d) => {
        if (err) console.log('Err: ' + err);
        else console.log('Saved ' + req.params.sr);
        res.status(200).send({
            'SR': 'OK'
        });
    })
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

function check_sr(req, res) {
    const days10 = 10 * 60 * 60 * 24 * 1000;
    var rsr = req.body['SR'];
    srdb.findOne({
        sr: rsr
    }, '-name', {
        lean: true
    }, (err, srdata) => {
        var present = 0; //console.log(rsr);
        if (err) {
            console.log(err);
        } else {
            if (srdata) {
                var diff = Date.now() - srdata['lmt'] * 1000;
                // avoid all SR polled at same time
                var sincelastdb = Date.now() - srdata['date'].getTime()
                var days30s = getRandomInt(30, 40) * 60 * 60 * 24 * 1000
                if (diff > days10 && sincelastdb < days30s)
                    present = 1;
            }
        }
        res.send({
            'present': present && !srdata['dirty'],
            'SR': rsr
        });
    })
}
