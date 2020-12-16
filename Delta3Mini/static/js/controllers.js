myapp.controller('IndexController', function ($scope, $http, $route, $cookies, BoardsService, $location, AuthService) {
    document.getElementById("registermenublock").hidden = true
    document.getElementById("loginmenublock").hidden = false

    //wszystko powyzej to wyswietlanie w menu (don't ask, you will be happier)

    $http.get('/api/list-boards').then(function (resp) {
        $scope.boards = resp.data.json_list;

        $scope.boards.sort(function(a,b) {
            if (a.archived === true && b.archived === false)
                return 1
            if (b.archived === true && a.archived === false)
                return -1

            return 0
        })

    }).catch(async function (response) {
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
        BoardsService.deleteBoard(id, $cookies.get('username'))
            .then(function () {
                $location.path('/')
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }
    $scope.archive = function (id) {
        BoardsService.archiveBoard(id, $cookies.get('username'))
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

    function retrive_board_info() {
        $http.get('/api/getBoardInfo', {params: {board_id: $routeParams.id}})
            .then(function (response) {
                $scope.boardInfo = response.data.board
            }).catch(function (response) {
            if (response.status === 401 && response.data['msg'] === "Token has expired") {
                AuthService.refreshToken()
            }
        })
    }

    var config = {params: {board_id: $routeParams.id}}

    function retrive_lists() {
        $http.get('/api/list-lists', config).then(async function (resp) {
            $scope.lists = resp.data.json_list;
            await retrive_board_info()
        }).catch(async function (response) {
            if (response.status === 401 && response.data['msg'] === "Token has expired") {
                await AuthService.refreshToken()
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

    //whatToChange to string, aktualnie mozna dać "content", "name", "date" i "done". Tak zrobiłem, don't judge me
    $scope.editCard = function (id, newCardContent, whatToChange) {
        console.log(newCardContent)
        BoardsService.editCard(newCardContent, id, whatToChange)
            .then(function () {
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

    $scope.changeLabelCheck = function (card_id, label_id) {
        BoardsService.addOrDeleteLabel(label_id, card_id)
            .then(function () {
                //$route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }


        /*if (this.labelCheckBox) {
            BoardsService.addOrDeleteLabel('add', label_id, card_id)
            .then(function () {
                //$route.reload()
                //this.labelCheckBox = true
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
        }
        else
        {
            // console.log("hello from changeLabel false")
            BoardsService.addOrDeleteLabel('delete', label_id, card_id)
            .then(function () {
                //$route.reload() teoretycznie nie musi go tu byc bo i tak sie odswiezy po zamknieciu okienka
                //this.labelCheckBox = false
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
        }
    }*/

    $scope.editLabelText = function (labelID, text)
    {
        //console.log("hello from editLabel")
        BoardsService.editLabelText(labelID, text)
            .then(function () {
                $route.reload()
            }, function () {
                $scope.errorMessage = 'Something went wrong'
            })
    }

    $scope.checkCheck = function (labels, labelID)
    {
        for(var label of labels)
        {
            //console.log(labelID + " " + label.id)
            if (label.id === labelID) {
                return true
            }
        }
        return false
    }

    //        DATE PICKER
    $scope.opened = {};

	$scope.open = function($event, elementOpened) {
		$event.preventDefault();
		$event.stopPropagation();

		$scope.opened[elementOpened] = !$scope.opened[elementOpened];
	};

	//DATE PICKER ENDS HERE

    //-------------------Showing and hiding modal windows in html
    $scope.showAddingCardForm = function (id) {
        $scope.list_id = id
        document.getElementById("addingCardForm").style.display = "block"
    }
    // initializing some variables in scope so that it works properly
    $scope.card_id = ''
    $scope.card_name = ''
    $scope.card_content = ''
    $scope.card_term = null
    $scope.card_done = false
    $scope.card_labels = []

    $scope.showEditCardForm = function (id, name, content, labels, term, done) {
        $scope.card_id = id
        $scope.card_name = name
        $scope.card_content = content
        $scope.card_labels = labels
        $scope.card_done = done
        $scope.card_term = term
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
        if (type == 'list element' && !external) {
            console.log('Container being dragged contains ' + callback() + ' items');
        }
        return index < 10; // Disallow dropping in the third row.
    };

    $scope.dropCallback = function (index, item, external, type) {
        console.log($scope.lists)
        // $scope.logListEvent('dropped at', index, external, type);
        console.log(item)
        console.log(index)
        console.log(external)
        console.log(type)
        // Return false here to cancel drop. Return true if you insert the item yourself.
         if (type == 'list') {
             console.log('Drop on AAAAAAAAAAAAAAA' + index + ' listy ' + item.index);
         }
        if (type == 'list' && !external) { //jaki typ to lista?
            console.log('Drop on AAAAAAAAAAAAAAA' + index + ' listy ' + item.index);
            BoardsService.patchListIndex(item.id, index)
                .then(function () {
                    //$route.reload()
                }, function () {
                    $scope.errorMessage = 'Something went wrong'
                })
        }
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

     $scope.showHiddenDateTime = function () {
        document.getElementById("hiddenDateTime").hidden = false
    }

})

myapp.controller("SinglePublicBoardController", function ($scope, $http, $routeParams, $route, $window, BoardsService, AuthService, $timeout) {
    var config = {params: {board_id: $routeParams.id}}

    function retrive_board_info() {
        $http.get('/api/getPublicBoardInfo', {params: {board_id: $routeParams.id}})
            .then(function (response) {
                $scope.boardInfo = response.data.board
            }).catch(function (response) {
            if (response.status === 401 && response.data['msg'] === "Token has expired") {
                AuthService.refreshToken()
            }
        })
    }

    function retrive_lists() {
        $http.get('/api/list-public-lists', config).then(async function (resp) {
            $scope.lists = resp.data.json_list;
            await retrive_board_info()
        }).catch(async function (response) {
            if (response.status === 401 && response.data['msg'] === "Token has expired") {
                await AuthService.refreshToken()
                retrive_lists()
            }
        })
    }

    retrive_lists()

    $window.onclick = function (event) {
        if (event.target === document.getElementById("addingCardForm")) {
            document.getElementById("addingCardForm").style.display = "none"
        }

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
})