(function () {
  'use strict';

  angular.module('app', [])

  .controller('ngappController', ['$scope', '$log',
    function($scope, $log) {
      $scope.getResults = function() {
        $log.log("test");
      };
    }
  ]);

}());