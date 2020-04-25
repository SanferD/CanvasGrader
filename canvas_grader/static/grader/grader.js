function InitializeGrader($scope, $http)
{

$scope.questions = GetValueJSON("questions")
$scope.quiz_id = GetValue("quiz-id")
$scope.canvas_users = GetValueJSON("canvas-users")

$scope.canvas_user_current = $scope.canvas_users[0]
$scope.canvas_user_selected = $scope.canvas_user_current

angular.element(Initialize)
function Initialize()
{
    $scope.questions.forEach(function(q) {
        var id = "Q" + q.question_id
        q_div = document.getElementById(id)
        q_div.innerHTML = q.question_text.trim()
    })
}

$scope.ChangeCurrentCanvasUser = function()
{
    console.log($scope.canvas_user_selected)
}

}
