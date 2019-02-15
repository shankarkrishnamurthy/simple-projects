const LocalStrategy = require('passport-local').Strategy;
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const User = mongoose.model('users');

function localfn(passport) {
    passport.use(new LocalStrategy({
        usernameField: 'email',
        passwordField: 'pass'
    }, (email, pass, done) => {
        // Match user
        User.findOne({
            email: email
        }).then(user => {
            if (!user) {
                return done(null, false, {
                    message: 'No User Found'
                });
            }

            bcrypt.compare(pass, user.pass, (err, isMatch) => {
                if (err) throw err;
                if (isMatch) {
                    return done(null, user);
                } else {
                    return done(null, false, {
                        message: 'Password Incorrect'
                    });
                }
            })
        })
    }));
    passport.serializeUser(function (user, done) {
        done(null, user.id);
    });
    passport.deserializeUser(function (id, done) {
        User.findById(id, function (err, user) {
            done(err, user);
        });
    });

}

module.exports = localfn;
