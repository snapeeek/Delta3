var myapp = angular.module("app", ['ngRoute', 'angular-loading-bar']);

myapp.config(function ($routeProvider, $locationProvider) {


    $routeProvider
        .when('/', {
            templateUrl: 'static/partials/index.html',
            controller: 'IndexController'
        })
        .when('/login', {
            templateUrl: 'static/partials/login.html',
            controller: 'LoginController'
        })
        .when('/register', {
            templateUrl: 'static/partials/register.html',
            controller: 'RegisterController'
        })
        .when('/logout', {
            controller: 'LogoutController'
        })
        .otherwise({
            redirect : '/'
        })



    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false});
    $locationProvider.hashPrefix('');


});

