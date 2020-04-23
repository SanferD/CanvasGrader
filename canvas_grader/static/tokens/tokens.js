var app = angular.module("canvas_grader", ["ngMaterial", "smart-table"])

app.controller("canvas_grader", function ($scope, $http) {

InitializePostHeaders($scope)

$scope.tokens_old = []
$scope.tokens = []

Initialize()

function Initialize()
{
    $http.get("tokens").then(function(resp) {
        $scope.tokens = resp.data.map(ServerToken2ClientToken)
        $scope.tokens_old = resp.data.map(ServerToken2ClientToken)
    })
}

function ServerToken2ClientToken(x)
{
    var token = x.token
    var domain = x.domain.url
    var id = x.id
    return {token: token, domain: domain, id: id}
}

$scope.AddRow = function()
{
    $scope.tokens.push({id: undefined})
}

$scope.RemoveRow = function(t)
{
    i = $scope.tokens.indexOf(t)
    if (i > -1)
        $scope.tokens.splice(i, 1)
}

$scope.Save = function()
{
    var to_save = GetTokensToSave()
    $http.post("tokens", {tokens: to_save}, {headers: $scope.post_headers})

    var to_delete = GetTokensToDelete()
    data = {tokens: to_delete}
    $http.delete("tokens", {headers: $scope.post_headers, data: data})
}

function GetTokensToSave()
{
    var to_save = []
    $scope.tokens.forEach(function(t_candidate) {
        var do_update = IsToken(t_candidate)
        for (var i = 0; i < $scope.tokens_old.length && do_update; i++) {
            var t_old = $scope.tokens_old[i]
            do_update = !EqualTokens(t_candidate, t_old)
        }
        if (do_update)
            to_save.push(t_candidate)
    })
    return to_save
}

function GetTokensToDelete()
{
    var to_delete = []
    $scope.tokens_old.forEach(function(t_old) {
        var is_removed = true
        for (var i = 0; i < $scope.tokens.length && is_removed; i++) {
            var t = $scope.tokens[i]
            is_removed = t_old.id != t.id
        }
        if (is_removed)
            to_delete.push(t_old)
    })
    return to_delete
}

function IsToken(t)
{
    return t !== undefined && "domain" in t && "token" in t
}

function EqualTokens(t1, t2)
{
    return t1.id == t2.id && t1.domain == t2.domain && t1.token == t2.token
}

}) 

