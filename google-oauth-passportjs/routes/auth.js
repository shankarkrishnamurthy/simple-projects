const express = require('express');
const passport = require('passport');
var router = express.Router();

router.get('/google', passport.authenticate('google', {
    scope: ['profile', 'email']
}));

router.get('/google/callback',
    passport.authenticate('google', {
        failureRedirect: '/'
    }), (req, res) => {
        console.log("in /auth/google/callback ok")
        res.redirect('/auth/dashboard');
    });

router.get('/dashboard', (req, res) => {
    var isa = JSON.stringify(req.isAuthenticated());
    res.send("/auth/dashboard ok     " + isa);
});

router.get('/verify', (req, res) => {
    var isa = JSON.stringify(req.isAuthenticated());
    if (req.user) {
        res.send(JSON.stringify(req.user) + '    ' + isa);
    } else {
        res.send('Not Auth    ' + isa);
    }
});

router.get('/logout', (req, res) => {
    req.logout();
    res.redirect('/');
});

module.exports = router;
