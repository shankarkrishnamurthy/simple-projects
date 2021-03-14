const GoogleStrategy = require('passport-google-oauth20').Strategy;
const keys = require('./keys');

var user = {
    id: null,
};

module.exports = function (passport) {
    var strataopt = {
        clientID: keys.googleClientID,
        clientSecret: keys.googleClientSecret,
        callbackURL: '/auth/google/callback',
        proxy: true
    };
    var stratacb = (accessToken, refreshToken, profile, done) => {
        console.log(accessToken);
        console.log(profile);
        console.log(refreshToken);
        console.log(done);
        user.id = profile.id;
        done(null, user);
    }

    var googlestrata = new GoogleStrategy(strataopt, stratacb);

    passport.use(googlestrata);

    passport.serializeUser((user, done) => {
        done(null, user.id);
    });

    passport.deserializeUser((id, done) => {
        //User.findById(id).then(user => done(null, user));
        done(null, user);
    });
};
