myapp.controller('IndexController', function ($scope, $http, $route, BoardsService, $location) {
    $http.get('/api/status').then(function (response) {
        document.getElementById("hello").innerText = "Hello " + response.data.username
        $scope.username = response.data.username
    })

    document.getElementById("registermenublock").hidden = true
    document.getElementById("loginmenublock").hidden = false

    //wszystko powyzej to wyswietlanie w menu (don't ask, you will be happier)

    $http.get('/api/list-boards').then(function (resp) {
        $scope.boards = resp.data.json_list;
    })

    $scope.generateBoard = function () {
        BoardsService.addBoard($scope.boardForm.name, $scope.boardForm.background, $scope.boardForm.team)
            .then(function () {
                $route.reload()
            })
            .catch(function () {
                $scope.error = true
                $scope.errorMessage = "Something went wrong during creating new board"
                $scope.disabled = false
                $scope.registerForm = {}
            })
    }

    $scope.delete = function (id) {
        BoardsService.deleteBoard(id, $scope.username)
            .then(function () {
                $location.path('/')
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }
    $scope.archive = function (id) {
        BoardsService.archiveBoard(id, $scope.username)
            .then(function () {
                $location.path('/')
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

})

myapp.controller('LoginController', function ($scope, $location, $route, AuthService) {
    $scope.login = function () {
        $scope.error = false
        $scope.disabled = true
        document.getElementById("loginmenublock").hidden = true
        document.getElementById("registermenublock").hidden = true
        AuthService.login($scope.loginForm.username, $scope.loginForm.password)
            .then(function () {
                $location.url('/')
                $scope.disabled = false
                $scope.loginForm = {}
            }, function () {
                $scope.error = true
                $scope.errorMessage = "Invalid username and/or password"
                $scope.disabled = false
                $scope.loginForm = {}
            })

    }

})

myapp.controller('RegisterController', function ($scope, $location, AuthService) {
    $scope.register = function () {
        $scope.error = false
        $scope.disabled = true
        document.getElementById("loginmenublock").hidden = true
        document.getElementById("registermenublock").hidden = true
        AuthService.register($scope.registerForm.email, $scope.registerForm.username, $scope.registerForm.password)
            .then(function () {
                $location.path('/login')
                $scope.disabled = false
                $scope.registerForm = {}
            })
            .catch(function () {
                $scope.error = true
                $scope.errorMessage = "Something went wrong"
                $scope.disabled = false
                $scope.registerForm = {}
            })
    }

})

myapp.controller('LogoutController', function ($scope, $location, $route, AuthService) {
    $scope.logout = function () {
        document.getElementById("loginmenublock").hidden = true
        document.getElementById("registermenublock").hidden = true
        AuthService.logout()
            .then(function () {
                $location.path('/login')
                //$route.reload()
            })
    }

})

myapp.controller("ngappController", function ($scope, $timeout, cfpLoadingBar, AuthService) {
    $timeout(callAtTimeout, 50);
    cfpLoadingBar.start();

    function callAtTimeout() {
        cfpLoadingBar.complete();
        $scope.help = AuthService.isLoggedIn()
    }
});

myapp.controller("SingleBoardController", function ($scope, $http, $routeParams, $route, $window, BoardsService) {
    var config = {params: {board_id: $routeParams.id}}
    $http.get('/api/list-lists', config).then(function (resp) {
        $scope.lists = resp.data.json_list;
    })

    $http.post('/api/getBoardInfo', {board_id: $routeParams.id})
        .then(function (response) {
            $scope.boardInfo = response.data.board
        })

    $scope.updateBoard = function (boardName) {
        if (boardName === "")
            boardName = $scope.boardInfo.name
        BoardsService.editBoard($scope.boardInfo.id, boardName)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

    $scope.unarchiveBoard = function (boardID) {
        BoardsService.unarchiveBoard(boardID)
         .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

    $scope.editList = function (id, boardName) {
        console.log("wchodze w edycje list")
        BoardsService.editList(id, boardName)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }


    $scope.generateList = function () {
        BoardsService.addList($scope.listForm.name, $routeParams.id)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

    $scope.generateCard = function (id) {
        BoardsService.addCardToList($scope.cardForm.name, id)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
        document.getElementById("cardForm").style.display = "none"
    }
    $scope.editCard = function (id) {
        BoardsService.editCardContent($scope.editCardForm.content, id)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
        document.getElementById("editCardForm").style.display = "none"
    }

    $scope.showModal = function (id) {
        $scope.list_id = id
        document.getElementById("cardForm").style.display = "block"
    }
    $scope.showCard = function (id, name, content) {
        $scope.card_id = id
        $scope.card_name = name
        $scope.card_content = content
        document.getElementById("editCardForm").style.display = "block"
    }

    $scope.hideModal = function () {
        document.getElementById("cardForm").style.display = "none"
    }

    $scope.dragoverCallback = function (index, external, type, callback) {
        $scope.logListEvent('dragged over', index, external, type);
        // Invoke callback to origin for container types.
        if (type == 'container' && !external) {
            console.log('Container being dragged contains ' + callback() + ' items');
        }
        return index < 10; // Disallow dropping in the third row.
    };

    $scope.dropCallback = function (index, item, external, type) {
        $scope.logListEvent('dropped at', index, external, type);
        // Return false here to cancel drop. Return true if you insert the item yourself.
        return item;
    };

    $scope.logEvent = function (message) {
        console.log(message);
    };

    $scope.logListEvent = function (action, index, external, type) {
        var message = external ? 'External ' : '';
        message += type + ' element was ' + action + ' position ' + index;
        console.log(message);
    };

    // Initialize model
    $scope.model = [[], []];
    var id = 10;
    angular.forEach(['all', 'move', 'copy', 'link', 'copyLink', 'copyMove'], function (effect, i) {
        var container = {items: [], effectAllowed: effect};
        for (var k = 0; k < 7; ++k) {
            container.items.push({label: effect + ' ' + id++, effectAllowed: effect});
        }
        $scope.model[i % $scope.model.length].push(container);
    });

    $scope.$watch('model', function (model) {
        $scope.modelAsJson = angular.toJson(model, true);
    }, true);

    $window.onclick = function (event) {
        if (event.target === document.getElementById("cardForm")) {
            document.getElementById("cardForm").style.display = "none"
        }
    }


})