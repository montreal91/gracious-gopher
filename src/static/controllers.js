
angular.module("myApp").controller("loginController",
    ["$scope", "$location", "AuthService",
    function ($scope, $location, AuthService) {
        console.log(AuthService.isLoggedIn());

        $scope.login = function() {
            $scope.error = false;
            $scope.disabled = true;

            AuthService.login($scope.loginForm.email, $scope.loginForm.password)
            .then(function () {
                $location.path("/");
                $scope.disabled = false;
                $scope.loginForm = {};
            })
            .catch(function () {
                $scope.error = true;
                $scope.errorMessage = "Invalid username or password";
                $scope.disabled = false;
                $scope.loginForm = {};
            });
        };
    }]
);

angular.module("myApp").controller("logoutController",
    ["$scope", "$location", "AuthService",
    function ($scope, $location, AuthService) {
        console.log(user);

        $scope.logout = function() {
            // console.log("foo.scope");
            AuthService.logout()
            .then(function() {
                $location.path("/login");
            });
        };
    }]
);

angular.module("myApp").controller("registerController",
    ["$scope", "$location", "AuthService",
    function ($scope, $location, AuthService) {
        $scope.register = function () {
            // Initial values
            $scope.error = false;
            $scope.disabled = true;

            // Call register from service
            console.log(AuthService);
            AuthService.register($scope.registerForm.email, $scope.registerForm.password)
            // Handle Success
            .then(function () {
                $location.path("/login");
                $scope.disabled = false;
                $scope.registerForm = {};
            })
            // Handle Error
            .catch(function () {
                $scope.error = true;
                $scope.errorMessage = "Something went wrong!";
                $scope.disabled = false;
                $scope.registerForm = {};
            });
        };
    }]
);
