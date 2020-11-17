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
                .then(function (data, status) {
                    if (status === 200 && data.result)
                    {
                        user = true;
                        deffered.resolve();
                    }
                    else
                    {
                        user = false
                        deffered.reject()
                    }
                })
                .catch(function (data) {
                    user = false
                    deffered.reject()
                })

            return deffered.promise
        }

        function logout() {
            var deffered = $q.defer()

            $http.get('/api/logout')
                .then(function (data) {
                    user = false
                    deffered.resolve()
                })
                .catch(function(data) {
                    user = false
                    deffered.reject()
                })
            return deffered.promise
        }

        function register(email, username, password) {
            var deffered = $q.defer()

            $http.post('/api/register', {email:email, username:username, password: password})
                .then(function (data, status) {
                    if (status === 200 && data.result)
                    {
                        deffered.resolve()
                    }
                    else
                    {
                        deffered.reject()
                    }
                })
                .catch(function (data) {
                    deffered.reject()

                })
            return deffered.promise
        }

        function getUserStatus() {
            return $http.get('/api/status')
                .then(function (data) {
                  if (data.status)
                      user = true
                  else
                      user = false
                })
                .catch(function (data) {
                    user = false
                })
        }

    }])