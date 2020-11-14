(function () {
    'use strict';

    angular.module('app', [])
        .controller('ngappController', ['$scope', '$log', '$timeout',
            function ($scope, $log, $timeout) {
                $scope.getResults = function () {
                    $log.log("test");
                    setTimeout(function () {
                        $log.log("abracadabra")
                    }, 2);

                };
            }
        ]);

}());


