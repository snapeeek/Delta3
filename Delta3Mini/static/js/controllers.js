myapp.controller('IndexController', function ($scope, $http) {
    $scope.message = "hello";
    $http.get('/api/list-records').then(function (resp) {
        $scope.tasks = resp.data.json_list;
    })
    document.getElementById("registermenublock").hidden = true
    document.getElementById("loginmenublock").hidden = false
    document.getElementById("hello").innerText = "Hello <insert user name>"

    //AuthService.

})

myapp.controller('LoginController', function ($scope, $location, $route, AuthService) {
    $scope.login = function () {
        $scope.error = false
        $scope.disabled = true
        document.getElementById("loginmenublock").hidden = true
        document.getElementById("registermenublock").hidden = true
        AuthService.login($scope.loginForm.username, $scope.loginForm.password)
            .then(function () {
                $location.url('/')
                $scope.disabled = false
                $scope.loginForm = {}
            }, function () {
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
        document.getElementById("loginmenublock").hidden = true
        document.getElementById("registermenublock").hidden = true
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

myapp.controller('LogoutController', function ($scope, $location, $route, AuthService) {
    $scope.logout = function () {
        document.getElementById("loginmenublock").hidden = true
        document.getElementById("registermenublock").hidden = true
        AuthService.logout()
            .then(function () {
                $location.path('/login')
                //$route.reload()
            })
    }

})

myapp.controller("DeleteController", function ($scope , $location, $route, TasksService) {
    $scope.delete = function (id) {
        TasksService.deleteTask(id)
            .then(function () {
                console.log(id)
                $location.path('/')
                $route.reload()
            }, function () {
                console.log(id)
                $scope.errorMessage = 'Something went wrong'
            })
    }
})

myapp.controller("ngappController", function ($scope, $timeout, cfpLoadingBar, AuthService) {
    $timeout(callAtTimeout, 50);
    //console.log("Makao");
    cfpLoadingBar.start();

    function callAtTimeout() {
        //console.log("Timeout occurred");
        cfpLoadingBar.complete();
        $scope.help = AuthService.isLoggedIn()
    }





});