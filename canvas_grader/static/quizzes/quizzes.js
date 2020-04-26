var app = angular.module("quizzes", ["ngMaterial", "smart-table"])

app.controller("quizzes", function ($scope, $http) {

$scope.imported = []
$scope.unimported = []
$scope.to_import = []
$scope.course_id = GetValue("course")

Initialize()
InitializePostHeaders($scope)
function Initialize()
{
    var api_quizzes = GetValueJSON("api-quizzes")
    var db_quizzes = GetValueJSON("db-quizzes")
    var db_quiz_ids = db_quizzes.map(function(x) { return x[0] })

    $scope.imported = []
    $scope.unimported = []
    api_quizzes.forEach(function(api_quiz) {
        var i = db_quiz_ids.indexOf(api_quiz[0])
        if (i == -1)
            $scope.unimported.push(api_quiz)
        else
            $scope.imported.push(api_quiz)
    })
}

$scope.exists = function(item)
{
    return $scope.to_import.indexOf(item) > -1
}

$scope.toggle = function(item)
{
    var i = $scope.to_import.indexOf(item)
    if (i == -1)
        $scope.to_import.push(item)
    else
        $scope.to_import.splice(i, 1)
}

$scope.Import = function()
{
    var url = "/courses/" + $scope.course_id + "/quizzes/import"
    $http({
        url: url,
        method: "POST",
        data: $scope.to_import,
        headers: $scope.post_headers
    }).then(function() { window.location.reload() })
}

}) 


