
angular.module("myApp").factory("AuthService",
    ["$q", "$timeout", "$http",
    function ($q, $timeout, $http) {
        var user = null;

        // Return available functions for use in controllers
        return ({
            isLoggedIn: isLoggedIn,
            login: login,
            logout: logout,
            register: register,
            getUserStatus: getUserStatus
        });

    function isLoggedIn() {
        if (user) {
            return true;
        } else {
            return false;
        }
    }

    function login(email, password) {
        // Create a new instance of deferred
        var deferred = $q.defer();

        $http.post("/api/login/", {email: email, password:password})
        .success(function (data, status) {
            if (status === 200 && data.result) {
                user = true;
                deferred.resolve();
            } else {
                user = false;
                deferred.reject();
            }
        })
        .error(function (data) {
            user = false;
            deferred.reject();
        });
        return deferred.promise;
    }

    function logout() {
        var deferred = $q.defer();

        $http.get("/api/logout/")
        .success(function (data) {
            user = false;
            deferred.resolve();
        })
        .error(function (data) {
            user = false;
            deferred.reject();
        });

        return deferred.promise;
    }

    function register(email, password) {
        var deferred = $q.defer();

        $http.post("/api/register/", {email: email, password: password})
        .success(function (data, status) {
            if (status === 200 && data.result) {
                deferred.resolve();
            } else {
                deferred.reject();
            }
        })
        .error(function(data) {
            deferred.reject();
        });
        return deferred.promise;
    }

    function getUserStatus() {
        return $http.get("/api/status/")
        .success(function (data){
            if (data.status) {
                user = true;
            } else {
                user = false;
            }
        })
        .error(function (data) {
            user = false;
        });
    }
}]);
