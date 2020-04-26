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

$scope.GetGradedCanvasUsers = function()
{
    var url = "/quizzes/" + $scope.quiz_id + "/grading-groups/" +
              $scope.grading_group_id + "/canvas-users/graded"
    return $http({
        url: url,
        method: "GET"
    })
}

$scope.SaveSubmission = function(submission)
{
    return $http({
        method: "POST",
        url: "/submission-data/" + submission.id + "/assessments",
        data: submission,
        headers: $scope.post_headers
    })
}

}

