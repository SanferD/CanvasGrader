function InitializeGrader($scope, $http)
{

$scope.questions = GetValueJSON("questions")
$scope.quiz_id = GetValue("quiz-id")
$scope.canvas_users = GetValueJSON("canvas-users")
console.log($scope.canvas_users)

Initialize()
function Initialize()
{
}

}
