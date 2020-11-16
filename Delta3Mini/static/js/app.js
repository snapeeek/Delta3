var myapp = angular.module("app", ['ngRoute','angular-loading-bar']);

myapp.config(function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('');

    $routeProvider
        .when('/', {
            templateUrl : 'static/partials/index.html',
            controller : 'IndexController'
        })
        .when('/login', {
            templateUrl : 'static/partials/login.html',
            controller : 'LoginController'
        })


});

