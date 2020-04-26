function InitializeGrader($scope, $http)
{

$scope.quiz_id = GetValue("quiz-id")
$scope.grading_group_id = GetValue("grading-group-id")

$scope.questions = GetValueJSON("questions")
$scope.canvas_users = []
$scope.canvas_user_current = undefined

$scope.submissions = {}
$scope.canvas_user_ids_graded = []

angular.element(Initialize)
function Initialize()
{
    $scope.questions.forEach(function(q) {
        var id = "Q" + q.id
        q_div = document.getElementById(id)
        q_div.innerHTML = q.question_text.trim()
        $scope.submissions[q.id] = {assessment: {comment: "", score: ""}}
    })
    $scope.GetGradedCanvasUsers().then(function(resp) {
        // this ordering matters to redraw the UI first time around
        $scope.canvas_user_ids_graded = resp.data
        $scope.canvas_users = GetValueJSON("canvas-users")
        $scope.canvas_user_selected = $scope.canvas_users[0]
        $scope.ChangeCurrentCanvasUser()
    })
}

$scope.IsGraded = function(canvas_user)
{
    return $scope.canvas_user_ids_graded.indexOf(canvas_user.id) > -1
}

var is_getting_graded_canvas_users = false
$scope.ChangeCurrentCanvasUser = function()
{
    $scope.canvas_user_current = $scope.canvas_user_selected
    $scope.GetSubmission($scope.canvas_user_current).then(function(resp) {
        resp.data.submissions.forEach(ShowSubmission)
    })
    if (!is_getting_graded_canvas_users) {
        is_getting_graded_canvas_users = true
        $scope.GetGradedCanvasUsers().then(function(resp) {
            $scope.canvas_user_ids_graded = resp.data
            is_getting_graded_canvas_users = false
        }, function(){ is_getting_graded_canvas_users = false })
    }
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

$scope.PreviousCanvasUser = function()
{
    if ($scope.canvas_user_current !== undefined) {
        var i = $scope.canvas_users.indexOf($scope.canvas_user_current)
        i = i - 1
        if (i < 0)
            i += $scope.canvas_users.length
        $scope.canvas_user_selected = $scope.canvas_users[i]
        $scope.ChangeCurrentCanvasUser()
    }
}

$scope.NextCanvasUser = function()
{
    if ($scope.canvas_user_current !== undefined) {
        var i = $scope.canvas_users.indexOf($scope.canvas_user_current)
        i = (i + 1) % $scope.canvas_users.length
        $scope.canvas_user_selected = $scope.canvas_users[i]
        $scope.ChangeCurrentCanvasUser()
    }
}

}
