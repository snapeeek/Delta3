myapp.controller('IndexController', function ($scope,$http) {
    $scope.message = "hello";
    console.log("test1213");
    $http.get('/page/list-records').then(function (resp) {
        console.log(resp.data.tasks);
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