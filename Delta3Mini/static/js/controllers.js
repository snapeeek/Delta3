myapp.controller('IndexController', function ($scope, $http) {
    $scope.message = "hello";
    $http.get('/api/list-records').then(function (resp) {
        $scope.tasks = resp.data.json_list;
    })

})

myapp.controller('LoginController', function ($scope, $location, AuthService) {
    $scope.login = function () {
        $scope.error = false
        $scope.disabled = true

        AuthService.login($scope.loginForm.username, $scope.loginForm.password)
            .then(function () {
                $location.path('/')
                $scope.disabled = false
                $scope.loginForm = {}

            })
            .catch(function () {
                $scope.error = true
                $scope.errorMessage = "Invalid username and/or password"
                $scope.disabled = false
                $scope.loginForm = {}
            })
    }

})

myapp.controller('RegisterController', function ($scope, $location, AuthService) {
    $scope.register = function () {
        $scope.error = false
        $scope.disabled = true

        AuthService.register($scope.registerForm.email, $scope.registerForm.username, $scope.registerForm.password)
            .then(function () {
                $location.path('/login')
                console.log($location.path())
                $scope.disabled = false
                $scope.registerForm = {}
            })
            .catch(function () {
                $scope.error = true
                $scope.errorMessage = "Something went wrong"
                $scope.disabled = false
                $scope.registerForm = {}
            })
    }

})

myapp.controller('LogoutController', function ($scope, $location, AuthService) {
    $scope.logout = function () {
        AuthService.logout()
            .then(function () {
                location.path('/login')
            })
    }

})

myapp.controller("ngappController", function ($scope, $timeout, cfpLoadingBar) {
    $timeout(callAtTimeout, 3000);
    console.log("Makao");
    cfpLoadingBar.start();

    function callAtTimeout() {
        console.log("Timeout occurred");
        cfpLoadingBar.complete();
    }

});