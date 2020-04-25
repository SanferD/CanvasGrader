function InitializeGrader($scope, $http)
{

$scope.questions = GetValueJSON("questions")
$scope.quiz_id = GetValue("quiz-id")
$scope.canvas_users = GetValueJSON("canvas-users")

$scope.canvas_user_current = undefined
$scope.canvas_user_selected = $scope.canvas_users[0]

$scope.submissions = []

angular.element(Initialize)
function Initialize()
{
    $scope.questions.forEach(function(q) {
        var id = "Q" + q.id
        q_div = document.getElementById(id)
        q_div.innerHTML = q.question_text.trim()
    })
    $scope.ChangeCurrentCanvasUser()
}

$scope.ChangeCurrentCanvasUser = function()
{
    console.log("change current user")
    $scope.canvas_user_current = $scope.canvas_user_selected
    $scope.GetSubmission($scope.canvas_user_current).then(function(resp) {
        $scope.submissions = resp.data.submissions
        $scope.submissions.forEach(ShowSubmission)
    })
}

function ShowSubmission(submission)
{
    var id = "A" + submission.quiz_question_id
    console.log(id)
    a_div = document.getElementById(id)
    if (a_div) {
        a_div.innerHTML = submission.text

        var assessment = submission.assessment
        var id = "C" + submission.quiz_question_id
        c_ta = document.getElementById(id)
        c_ta.innerText = assessment? assessment.comment: ""
    }
}

}
