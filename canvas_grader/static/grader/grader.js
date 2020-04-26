function InitializeGrader($scope, $http)
{

$scope.questions = GetValueJSON("questions")
$scope.quiz_id = GetValue("quiz-id")
$scope.canvas_users = GetValueJSON("canvas-users")

$scope.canvas_user_current = undefined
$scope.canvas_user_selected = $scope.canvas_users[0]

$scope.submissions = {}

angular.element(Initialize)
function Initialize()
{
    $scope.questions.forEach(function(q) {
        var id = "Q" + q.id
        q_div = document.getElementById(id)
        q_div.innerHTML = q.question_text.trim()
        $scope.submissions[q.id] = {assessment: {comment: "", score: ""}}
    })
    $scope.ChangeCurrentCanvasUser()
}

$scope.ChangeCurrentCanvasUser = function()
{
    $scope.canvas_user_current = $scope.canvas_user_selected
    $scope.GetSubmission($scope.canvas_user_current).then(function(resp) {
        resp.data.submissions.forEach(ShowSubmission)
    })
}

function ShowSubmission(submission)
{
    var q_id = submission.quiz_question_id
    var id = "A" + q_id
    a_div = document.getElementById(id)
    if (a_div) {
        a_div.innerHTML = submission.text

        if (submission.assessment === null)
            submission.assessment = {comment: "", score: ""}
    }
    $scope.submissions[q_id] = submission
}

}
