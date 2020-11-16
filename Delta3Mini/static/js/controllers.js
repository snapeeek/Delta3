myapp.controller('IndexController', function ($scope,$http) {
    $scope.message = "hello";
    $http.get('/page/list-records').then(function (resp) {
        $scope.tasks = resp.data.json_list;
    })

})

myapp.controller('LoginController', function ($scope) {
    $scope.afterClick = function($location) {
        $location.path('/register')
    }
})

myapp.controller('RegisterController', function ($scope) {
    $scope.message = 'hello';
})

myapp.controller('LogoutController', function ($scope, $route) {
    $route.reload()
    $route.current()

})

myapp.controller("ngappController", function($scope, $timeout, cfpLoadingBar){
    $timeout(callAtTimeout, 3000);
    console.log("Makao");
    cfpLoadingBar.start();

    function callAtTimeout() {
    console.log("Timeout occurred");
    cfpLoadingBar.complete();
    }

});