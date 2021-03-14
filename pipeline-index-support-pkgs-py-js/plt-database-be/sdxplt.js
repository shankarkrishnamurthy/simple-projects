const express = require('express'),
    app = express();
const exphbs = require('express-handlebars')
const bodyParser = require('body-parser');
const flash = require('connect-flash');
const path = require('path');
const fs = require('fs');
const doAsync = require('doasync');
const xjs = require('xml-js')
const session = require('express-session');


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
app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true,
}));


app.use(express.static(path.join(__dirname, '/public')));
app.use(flash());
app.use(function (req, res, next) {
    res.locals.success_msg = req.flash('success_msg');
    res.locals.error_msg = req.flash('error_msg');
    res.locals.error = req.flash('error');
    res.locals.user = req.user || null;
    next();
});

var port = process.env.PORT || 2568;
app.route('/').get(home);
app.route('/list').get(list);
app.route('/:id').get(show);
app.listen(port);

function home(req, res) {
    res.redirect('/list');
}

function getobj(fl) {
    var h = []
    for (i in fl) {
        var a = fl[i].split('/')
        if (a.length > 2)
            h.push({
                'ID': a[2],
                'CN': a[1],
                'FD': fl[i]
            })
    }

    return h;
}

function list(req, res) {
    var fl = walkSync('platforms')
    var h = getobj(fl)

    res.render('list', {
        pl: h
    })
}

var walkSync = function (dir, filelist) {
    var path = path || require('path');
    var fs = fs || require('fs'),
        files = fs.readdirSync(dir);
    filelist = filelist || [];
    files.forEach(function (file) {
        if (fs.statSync(path.join(dir, file)).isDirectory()) {
            filelist = walkSync(path.join(dir, file), filelist);
        } else {
            if (file == 'sdx-def.xml')
                filelist.push(path.join(dir, file));
        }
    });
    return filelist;
};

function show(req, res) {
    var fl = walkSync('platforms')
    var h = getobj(fl)
    var i;
    for (i in h) {
        if (h[i]['ID'] == req.params.id) break;
    }
    if (!(i in h) || (h[i]['ID'] != req.params.id)) {
        var msg = 'Platform ID ' + req.params.id + ' not found';
        req.flash('error_msg', msg)
        res.redirect("/list")
    } else {
        var p = h[i]['FD']
        doAsync(fs).readFile(p)
            .then((data) => {
                var s = Buffer.from(data).toString('utf-8')
                if ('f' in req.query && req.query['f'] == 'json') {
                    var jobj = xjs.xml2json(s, {
                        compact: true,
                        spaces: 4
                    });
                    //console.log(jobj)
                    res.setHeader('content-type', 'application/json');
                    res.send(jobj)
                } else {
                    res.setHeader('content-type', 'application/xml');
                    res.send(s)
                }
            })
    }
}
