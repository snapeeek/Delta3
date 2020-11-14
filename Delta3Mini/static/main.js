var myapp = angular.module("app", ['angular-loading-bar']);

myapp.controller("ngappController", function($scope, $timeout, cfpLoadingBar){
    $timeout(callAtTimeout, 3000);
    console.log("Makao");
    cfpLoadingBar.start();

    function callAtTimeout() {
    console.log("Timeout occurred");
    cfpLoadingBar.complete();
    }

});