angular.module('app').factory('AuthService',
    ['$q', '$timeout', '$http',
    function ($q, $timeout, $http) {

    var user = null;

        return ({
            isLoggedIn: isLoggedIn,
            login: login,
            logout: logout,
            register: register,
            getUserStatus: getUserStatus
        });

        function isLoggedIn() {
            if (user)
            {
                return true
            }
            else
            {
                return false
            }
        }

        function login(username, password) {
            var deffered = $q.defer();

            $http.post('/api/login', {username: username, password: password})
                .then(function (response) {
                    if (response.data)
                    {
                        user = true;
                        deffered.resolve();
                    }
                    else
                    {
                        user = false
                        deffered.reject()
                    }
                }, function (response) {
                    user = false
                    deffered.reject()
                })

            return deffered.promise
        }

        function logout() {
            var deffered = $q.defer()

            $http.get('/api/logout')
                .then(function (response) {
                    user = false
                    deffered.resolve()
                }, function(response) {
                    user = false
                    deffered.reject()
                })
            return deffered.promise
        }

        function register(email, username, password) {
            var deffered = $q.defer()

            $http.post('/api/register', {email:email, username:username, password: password})
                .then(function (response) {
                    if (response.data)
                    {
                        deffered.resolve()
                    }
                    else
                    {
                        deffered.reject()
                    }
                })
                .catch(function (response) {
                    deffered.reject()

                })
            return deffered.promise
        }

        function getUserStatus() {
            return $http.get('/api/status')
                .then(function (response) {
                  if (response.data.status) {
                      user = true
                  }
                  else
                      user = false
                }, function (response) {
                    user = false
                })
        }

    }])

angular.module('app').factory('BoardsService',
    ['$q', '$timeout', '$http',
        function ($q, $timeout, $http) {
            return ({
                deleteBoard: deleteBoard,
                archiveBoard: archiveBoard,
                addBoard: addBoard,
                addList: addList,
                addCardToList: addCardToList,
                editCardContent:editCardContent,

            })

            function deleteBoard(id, username) {
                var deffered = $q.defer()

                $http.post('/api/delete', {id: id, username: username})
                    .then(function (response) {
                        if (response.data)
                            deffered.resolve()
                        else
                            deffered.reject()

                    }, function (response) {
                        deffered.reject()
                    })
                return deffered.promise

            }

            function archiveBoard(id, username) {
                var deffered = $q.defer()

                $http.post('/api/archive', {id: id, username: username})
                    .then(function (response) {
                        if (response.data)
                            deffered.resolve()
                        else
                            deffered.reject()

                    }, function (response) {
                        deffered.reject()
                    })
                return deffered.promise

            }

            function addBoard(name, background, team) {
            var deffered = $q.defer()

            $http.post('/api/generateBoard', {name:name, background:background, team_id: team})
                .then(function (response) {
                    if (response.data)
                    {
                        deffered.resolve()
                    }
                    else
                    {
                        deffered.reject()
                    }
                })
                .catch(function (response) {
                    deffered.reject()

                })
            return deffered.promise
            }
            function addList(name, boardID ) {
            var deffered = $q.defer()

            $http.post('/api/generateList', {name:name,  board_id: boardID})
                .then(function (response) {
                    if (response.data)
                    {
                        deffered.resolve()
                    }
                    else
                    {
                        deffered.reject()
                    }
                })
                .catch(function (response) {
                    deffered.reject()

                })
            return deffered.promise
            }
            function addCardToList(name, listID ) {
            var deffered = $q.defer()

            $http.post('/api/generateCard', {name:name,  list_id: listID})
                .then(function (response) {
                    if (response.data)
                    {
                        deffered.resolve()
                    }
                    else
                    {
                        deffered.reject()
                    }
                })
                .catch(function (response) {
                    deffered.reject()

                })
            return deffered.promise
            }
            function editCardContent(content, cardID ) {
            var deffered = $q.defer()

            $http.post('/api/editCard', {content:content,  card_id: cardID})
                .then(function (response) {
                    if (response.data)
                    {
                        deffered.resolve()
                    }
                    else
                    {
                        deffered.reject()
                    }
                })
                .catch(function (response) {
                    deffered.reject()

                })
            return deffered.promise
            }
        }])