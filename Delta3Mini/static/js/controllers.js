myapp.controller('IndexController', function ($scope, $http) {
    $scope.myitems = [];
    $http.get('/getlist').then(function(resp) {
        $scope.myitems = resp.data.tasks
    })
    console.log($scope.myitems)
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