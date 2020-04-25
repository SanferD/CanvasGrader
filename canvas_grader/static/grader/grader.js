function InitializeGrader($scope, $http)
{

$scope.questions = GetValueJSON("questions")
$scope.quiz_id = GetValue("quiz-id")
$scope.canvas_users = GetValueJSON("canvas-users")

$scope.canvas_user_current = $scope.canvas_users[0]
$scope.canvas_user_selected = $scope.canvas_user_current

$scope.ChangeCurrentCanvasUser = function()
{
    console.log($scope.canvas_user_selected)
}


}
