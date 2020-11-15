var myapp = angular.module("app", ['ngRoute','angular-loading-bar']);

myapp.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl : 'static/index.html',
            controller : 'IndexController'
        })
        .when('/login', {
            templateUrl : 'static/login.html',
            controller : 'LoginController'
        })
    $locationProvider.hashPrefix('');

})

myapp.controller('IndexController', function ($scope) {
    $scope.message = "hello";
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