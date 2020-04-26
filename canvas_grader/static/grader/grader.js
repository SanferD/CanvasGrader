function InitializeGrader($scope, $http)
{

$scope.quiz_id = GetValue("quiz-id")
$scope.grading_group_id = GetValue("grading-group-id")

$scope.questions = GetValueJSON("questions")
$scope.canvas_users = []
$scope.canvas_user_current = undefined

$scope.submissions = {}
$scope.canvas_user_ids_graded = []

$scope.show_loading_msg = false
$scope.show_saving_msg = false

var autosave_timer = {};
angular.element(Initialize)
function Initialize()
{
    $scope.questions.forEach(function(q) {
        var id = "Q" + q.id
        q_div = document.getElementById(id)
        q_div.innerHTML = q.question_text.trim()
        $scope.submissions[q.id] = {assessment: {comment: "", score: ""}}
        autosave_timer[q.id] = undefined
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

var is_waiting = false
$scope.ChangeCurrentCanvasUser = function()
{
    if (HasTimer()) {
        if (!is_waiting) {
            is_waiting = true
            setTimeout(function() {
                is_waiting = false
                $scope.ChangeCurrentCanvasUser()
            }, 500)
        }
    } else {
        ChangeCanvasUser()
    }

    $scope.show_saving_msg = is_waiting
}

var is_getting_graded_canvas_users = false
function ChangeCanvasUser()
{
    $scope.canvas_user_current = $scope.canvas_user_selected
    $scope.show_loading_msg = true
    $scope.GetSubmission($scope.canvas_user_current).then(function(resp) {
        resp.data.submissions.forEach(ShowSubmission)
        $scope.show_loading_msg = false
    })
    if (!is_getting_graded_canvas_users) {
        is_getting_graded_canvas_users = true
        $scope.GetGradedCanvasUsers().then(function(resp) {
            $scope.canvas_user_ids_graded = resp.data
            is_getting_graded_canvas_users = false
        }, function(){ is_getting_graded_canvas_users = false })
    }
}

function HasTimer()
{
    for (var x in autosave_timer)
        if (autosave_timer[x] !== undefined)
            return true
    return false
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

var AUTOSAVE_INTERVAL_MS = 1300;
$scope.OnScoreChange = function(submission)
{
    OnChange(submission)
}

$scope.OnCommentChange = function(submission)
{
    OnChange(submission)
}

function OnChange(submission)
{
    var id = submission.quiz_question_id
    clearTimeout(autosave_timer[id])
    autosave_timer[id] = setTimeout(function() {
        Save(submission)
    }, AUTOSAVE_INTERVAL_MS)
}

function Save(submission)
{
    $scope.SaveSubmission(submission).then(function(resp) {
        autosave_timer[submission.quiz_question_id] = undefined
    })
}

}
