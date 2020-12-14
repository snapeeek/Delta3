angular.module('app').factory('AuthService',
    ['$q', '$timeout', '$http', '$cookies', '$window', '$route',
        function ($q, $timeout, $http, $cookies, $window, $route) {

            var user = null;

            return ({
                isLoggedIn: isLoggedIn,
                login: login,
                logout: logout,
                register: register,
                getUserStatus: getUserStatus,
                refreshToken: refreshToken,
                reloadHeader: reloadHeader
            });

            function isLoggedIn() {
                if (user) {
                    return true
                } else {
                    return false
                }
            }

            function login(username, password) {
                var deffered = $q.defer();

                $http.post('/api/login', {username: username, password: password})
                    .then(function (response) {
                        if (response.data['result']) {
                            user = true;
                            let access_token = response.data['access_token'];
                            let refresh_token = response.data['refresh_token'];

                            $window.localStorage.setItem("refresh_token", refresh_token);
                            $http.defaults.headers.common.Authorization = 'Bearer ' + access_token;

                            $cookies.put('access_token', access_token)
                            $cookies.put('username', username)
                            deffered.resolve();
                        } else {
                            user = false
                            deffered.reject()
                        }
                    }, function (response) {
                        user = false
                        deffered.reject()
                    })

                return deffered.promise
            }

            function reloadHeader() {
                let access_token = $cookies.get('access_token');
                $http.defaults.headers.common.Authorization = 'Bearer ' + access_token;
            }


            function logout() {
                var deffered = $q.defer()

                $http.get('/api/logout')
                    .then(function (response) {
                        user = false
                        deffered.resolve()
                    }, function (response) {
                        user = false
                        deffered.resolve()
                    })
                return deffered.promise
            }

            function register(email, username, password) {
                var deffered = $q.defer()

                $http.post('/api/register', {email: email, username: username, password: password})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
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
                            document.getElementById("hello").innerText = "Hello " + response.data.username
                            user = true
                        } else
                            user = false
                    }, function (response) {
                        user = false
                    })
            }

            async function refreshToken() {
                let refresh_token = $window.localStorage.getItem('refresh_token')
                $http.defaults.headers.common.Authorization = 'Bearer ' + refresh_token;
                let old_access_token = $cookies.get('access_token')
                await $http.post('/api/refresh_token', {access_token: old_access_token})
                    .then(function (responseFromPost) {
                        access_token = responseFromPost.data['access_token']
                        $http.defaults.headers.common.Authorization = 'Bearer ' + access_token;
                        $cookies.put('access_token', access_token)
                        $route.reload()
                    })
            }

        }])

angular.module('app').factory('BoardsService',
    ['$q', '$timeout', '$http', 'AuthService',
        function ($q, $timeout, $http, AuthService) {
            return ({
                deleteBoard: deleteBoard,
                archiveBoard: archiveBoard,
                addBoard: addBoard,
                editBoard: editBoard,
                addList: addList,
                addCardToList: addCardToList,
                addOrDeleteLabel: addOrDeleteLabel,
                editCard: editCard,
                unarchiveBoard: unarchiveBoard,
                editList: editList,
                editLabelText: editLabelText,
            })

            function deleteBoard(id, username) {
                var deffered = $q.defer()

                $http.post('/api/delete', {id: id, username: username})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve();
                        } else
                            deffered.reject()

                    }, function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                deleteBoard(id, username)
                            })
                        }
                        deffered.reject()
                    })
                return deffered.promise

            }

            function archiveBoard(id, username) {
                var deffered = $q.defer()

                $http.post('/api/archive', {id: id, username: username})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }

                    }, function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                archiveBoard(id, username)
                            })

                        }
                        deffered.reject()
                    })
                return deffered.promise
            }

            function addBoard(name, background, team) {
                var deffered = $q.defer()

                $http.post('/api/generateBoard', {name: name, background: background, team_id: team})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                addBoard(name, background, team)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function editBoard(boardID, boardName) {
                var deffered = $q.defer()

                $http.post('/api/editBoard', {board_id: boardID, name: boardName})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                editBoard(boardID, boardName)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function addList(name, boardID) {
                var deffered = $q.defer()

                $http.post('/api/generateList', {name: name, board_id: boardID})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                addList(name, boardID)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function addOrDeleteLabel(labelID, cardID) {
                var deffered = $q.defer()

                $http.post('/api/addOrDeleteLabel', {cardID: cardID, labelID: labelID})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                addOrDeleteLabel( labelID, cardID)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function addCardToList(name, listID) {
                var deffered = $q.defer()

                $http.post('/api/generateCard', {name: name, list_id: listID})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                addCardToList(name, listID)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function editCard(content, cardID, whatToChange) {
                var deffered = $q.defer()

                $http.post('/api/editCard', {content: content, card_id: cardID, what: whatToChange})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                editCard(content, cardID, whatToChange)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function unarchiveBoard(boardID) {
                var deffered = $q.defer()
                $http.post('/api/unarchiveBoard', {board_id: boardID})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                unarchiveBoard(boardID)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function editList(listID, listName) {
                var deffered = $q.defer()
                $http.post('/api/editList', {list_id: listID, list_name: listName})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                editList(listID, listName)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }

            function editLabelText(labelID, text) {
                var deffered = $q.defer()
                $http.post('/api/editLabelText', {label_id: labelID, text: text})
                    .then(function (response) {
                        if (response.data) {
                            deffered.resolve()
                        } else {
                            deffered.reject()
                        }
                    })
                    .catch(function (response) {
                        if (response.status === 401 && response.data['msg'] === "Token has expired") {
                            AuthService.refreshToken().then(function () {
                                editLabelText(labelID, text)
                            })
                        }
                        deffered.reject()

                    })
                return deffered.promise
            }
        }])