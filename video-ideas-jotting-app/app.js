const express = require('express');
const exphbs = require('express-handlebars');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const methodOverride = require('method-override');
const flash = require('connect-flash');
const passport = require('passport');
const session = require('express-session');

const indexRouter = require('./routes/index');
const aboutRouter = require('./routes/about');
const ideasRouter = require('./routes/ideas');
const usersRouter = require('./routes/users');

require('./config/passport')(passport);

var app = express();

// connect to mongoose
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/video-ideas', {
        useNewUrlParser: true
    })
    .then(() => console.log("Connecting to DB succeeded"))
    .catch(() => console.log("DB connect Error"));

app.engine('handlebars', exphbs({
    defaultLayout: 'main'
}));
app.set('view engine', 'handlebars');

app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
app.use(methodOverride('_method'));
app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true,
}));

app.use(passport.initialize());
app.use(passport.session());

app.use(flash());
app.use(function (req, res, next) {
    res.locals.success_msg = req.flash('success_msg');
    res.locals.error_msg = req.flash('error_msg');
    res.locals.error = req.flash('error');
    res.locals.user = req.user || null;
    next();
});

app.use('/', indexRouter);
app.use('/about', aboutRouter);
app.use('/ideas', ideasRouter);
app.use('/users', usersRouter);

module.exports = app;
