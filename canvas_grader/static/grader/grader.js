function InitializeGrader($scope, $http)
{

$scope.questions = GetValueJSON("questions")
$scope.quiz_id = GetValue("quiz-id")

Initialize()
function Initialize()
{
    $scope.GetCanvasUsers().then(function(resp) {
        var canvas_users = resp.data
        console.log(canvas_users)
    })
}

}
