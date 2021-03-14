var express = require('express');
var route = express.Router();

/* GET users listing. Dont put 'already mentioned app.use route again' */
route.get('/', function (req, res, next) {
    res.render('about');
});

module.exports = route;
