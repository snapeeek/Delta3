myapp.controller('IndexController', function ($scope, $http, $route, BoardsService, $location, AuthService) {
    document.getElementById("registermenublock").hidden = true
    document.getElementById("loginmenublock").hidden = false

    //wszystko powyzej to wyswietlanie w menu (don't ask, you will be happier)

    $http.get('/api/list-boards').then(function (resp) {
        $scope.boards = resp.data.json_list;
    }).catch( async function (response) {
        if (response.status === 401 && response.data['msg'] === "Token has expired") {
           await AuthService.refreshToken()
        }
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
    $scope.openBoardForm = function () {
        document.getElementById("boardForm").style.display = "block"
    }
    $scope.hideBoardForm = function () {
        document.getElementById("boardForm").style.display = "none"
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

myapp.controller("SingleBoardController", function ($scope, $http, $routeParams, $route, $window, BoardsService, AuthService, $timeout) {
    var config = {params: {board_id: $routeParams.id}}
    function retrive_board_info () {
        $http.get('/api/getBoardInfo', {params: {board_id: $routeParams.id}})
            .then(function (response) {
                $scope.boardInfo = response.data.board
            }).catch(function (response) {
            if (response.status === 401 && response.data['msg'] === "Token has expired") {
                AuthService.refreshToken()
            }
        })
    }
    function retrive_lists() {
        $http.get('/api/list-lists', config).then(async function (resp) {
            $scope.lists = resp.data.json_list;
            await retrive_board_info()
        }).catch(async  function (response) {
            if (response.status === 401 && response.data['msg'] === "Token has expired") {
               await  AuthService.refreshToken()
                retrive_lists()
            }

        })
    }
    retrive_lists()

    //
    // async function retrive_board_info() {
    //
    // }


    //-------------------functions to change board states
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

    //-------------------editing lists and cards done through submitting of forms in board.html
    $scope.generateList = function () {
        BoardsService.addList(this.addingListForm.name, $routeParams.id)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }
    $scope.editList = function (id, newListName) {
        BoardsService.editList(id, newListName)
            .then(function () {
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

    $scope.generateCard = function (id) {
        BoardsService.addCardToList(this.addingCardForm.name, id)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
        document.getElementById("addingCardForm").style.display = "none"
    }

    $scope.addLabel = function (cardId) {
        BoardsService.addLabelToCard(this.addLabel.id, cardId)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })

    }

    $scope.editCard = function (id, newCardContent) {
        BoardsService.editCard(newCardContent, id)
            .then(function () {
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

    //-------------------Showing and hiding modal windows in html
    $scope.showAddingCardForm = function (id) {
        $scope.list_id = id
        document.getElementById("addingCardForm").style.display = "block"
    }
    // initializing some variables in scope so that it works properly
    $scope.card_id = ''
    $scope.card_name = ''
    $scope.card_content = ''

    $scope.showEditCardForm = function (id, name, content) {
        $scope.card_id = id
        $scope.card_name = name
        $scope.card_content = content
        document.getElementById("editCardForm").style.display = "block"
    }
    $scope.showListForm = function () {
        document.getElementById("addingListForm").style.display = "block"
    }

    //simple hiding methods
    $scope.hideAddingCardForm = function () {
        document.getElementById("addingCardForm").style.display = "none"
    }
    $scope.hideEditCardForm = function () {
        document.getElementById("editCardForm").style.display = "none"
        $route.reload()
    }
    $scope.hideListForm = function () {
        document.getElementById("addingListForm").style.display = "none"
    }

    //-------------------funtions to be used when draging will be implemented for now they just log messages
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

    $window.onclick = function (event) {
        if (event.target === document.getElementById("addingCardForm")) {
            document.getElementById("addingCardForm").style.display = "none"
        }

    }

})