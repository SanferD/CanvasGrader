function InitializeGraderAPI($scope, $http)
{

InitializePostHeaders($scope)

$scope.GetSubmission = function(canvas_user)
{
    var url = "/quizzes/" + $scope.quiz_id + "/submissions"
    return $http({
        url: url,
        method: "GET",
        params: {"canvas-user": canvas_user.id}
    })
}

}

