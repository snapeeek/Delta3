myapp.controller('IndexController', function ($scope,$http) {
    $scope.message = "hello";
    $http.get('/page/list-records').then(function (resp) {
        $scope.tasks = resp.data.json_list;
    })

})

myapp.controller('LoginController', function ($scope) {
    $scope.message = "hello from Login";

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