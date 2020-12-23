var myapp = angular.module("app", ['ngRoute', 'angular-loading-bar', 'dndLists', 'xeditable','ngCookies', 'ui.bootstrap']);

myapp.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'static/partials/index.html',
            controller: 'IndexController',
            access: {restricted: true}
        })
        .when('/login', {
            templateUrl: 'static/partials/login.html',
            controller: 'LoginController',
            access: {restricted: false}
        })
        .when('/register', {
            templateUrl: 'static/partials/register.html',
            controller: 'RegisterController',
            access: {restricted: false}
        })
        .when('/logout', {
            controller: 'LogoutController',
            access: {restricted: true}
        })
        .when('/board/:id', {
            templateUrl: 'static/partials/board.html',
            controller: 'SingleBoardController',
            access: {restricted: true}
        })
        .when('/publicBoard/:id', {
            templateUrl: 'static/partials/publicBoard.html',
            controller: 'SinglePublicBoardController',
            access: {restricted: false}
        })
        .when('/delete/:id', {
            controller: 'DeleteController',
            access: {restricted: true}
        })
        .otherwise({
            redirect: '/'
        })

    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });
    $locationProvider.hashPrefix('');
});

myapp.run(function ($rootScope, $location, $route, AuthService, editableOptions) {
    $rootScope.$on('$routeChangeStart',
        function (event, next, current) {
            AuthService.getUserStatus()
                .then(function () {
                    if (next.access.restricted && !AuthService.isLoggedIn()) {
                        console.log(AuthService.isLoggedIn())
                        $location.path('/login')
                        $route.reload()
                    }
                })
        })
    AuthService.reloadHeader()
    editableOptions.theme = 'bs3'
})

