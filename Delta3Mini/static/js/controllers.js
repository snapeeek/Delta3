myapp.controller('IndexController', function ($scope, $http) {
    $http.get('/api/status').then(function (response) {
        document.getElementById("hello").innerText = "Hello " + response.data.username
    })

    document.getElementById("registermenublock").hidden = true
    document.getElementById("loginmenublock").hidden = false

    //wszystko powyzej to wyswietlanie w menu (don't ask, you will be happier)

    $http.get('/api/list-boards').then(function (resp) {
        $scope.boards = resp.data.json_list;
        console.log(resp.data);
    })


    



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

myapp.controller("DeleteController", function ($scope , $location, $route, BoardsService) {
    $scope.delete = function (id) {
        BoardsService.deleteBoard(id)
            .then(function () {
                $location.path('/')
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }
})

myapp.controller("ngappController", function ($scope, $timeout, cfpLoadingBar, AuthService) {
    $timeout(callAtTimeout, 50);
    cfpLoadingBar.start();

    function callAtTimeout() {
        cfpLoadingBar.complete();
        $scope.help = AuthService.isLoggedIn()
    }
});

myapp.controller("SingleBoardController", function ($scope , $http) {
    var config  ={ params:{board_id: 1}}
    //todo repalce board id with some kind of variable
    $http.get('/api/list-lists', config).then(function (resp) {
        $scope.lists = resp.data.json_list;
        console.log(resp.data);
    })
})