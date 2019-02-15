const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const passport = require('passport');
const route = express.Router();
require('../models/User');
const User = mongoose.model('users');

route.get('/login', function (req, res, next) {
    res.render('users/login');
});

route.get('/register', function (req, res, next) {
    res.render('users/register');
});
route.get('/logout', function (req, res, next) {
    req.logout();
    req.flash('success_msg', 'User is successfully logged out');
    res.redirect('/users/login');
});
route.post('/login', function (req, res, next) {
    passport.authenticate('local', {
        successRedirect: '/ideas',
        failureRedirect: '/users/login',
        failureFlash: true
    })(req, res, next);
});

route.post('/register', function (req, res, next) {
    let errors = [];

    if (req.body.pass != req.body.pass2) {
        errors.push({
            text: 'Passwords do not match'
        });
    }

    if (req.body.pass.length < 4) {
        errors.push({
            text: 'Password must be at least 4 characters'
        });
    }

    if (errors.length > 0) {
        res.render('users/register', {
            errors: errors,
            name: req.body.name,
            email: req.body.email,
            pass: req.body.pass,
            pass2: req.body.pass2
        });
    } else {
        User.findOne({
                email: req.body.email
            })
            .then(user => {
                if (user) {
                    req.flash('error_msg', 'Email already regsitered');
                    res.redirect('/users/register');
                } else {
                    const nuser = new User({
                        name: req.body.name,
                        email: req.body.email,
                        pass: req.body.pass
                    });
                    bcrypt.genSalt(10, (err, salt) => {
                        if (err) throw err;
                        bcrypt.hash(req.body.pass, salt, function (err, hash) {
                            if (err) throw err;
                            nuser.pass = hash
                            nuser.save()
                                .then(idea => {
                                    req.flash('success_msg', 'You are now registered. Pls login');
                                    res.redirect('/users/login');
                                })
                                .catch(err => {
                                    throw err;
                                });
                        });
                    });
                }
            });
    }
});
module.exports = route;
