function InitializeGraderAPI($scope, $http)
{

InitializePostHeaders($scope)

$scope.GetCanvasUsers = function()
{
    var url = '/quizzes/' + $scope.quiz_id + '/canvas-users'
    return $http({
        method: "GET",
        url: url,
    })
}

}

