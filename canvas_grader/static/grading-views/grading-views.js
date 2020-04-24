var app = angular.module("grading-views", ["ngMaterial", "smart-table"])

app.controller("grading-views", function ($scope, $http) {

$scope.grading_view = {
    name: "",
    grading_groups: []
}
$scope.all_questions = []
$scope.show_duplicate_questions_errmsg = false
$scope.show_invalid_name = false
$scope.show_missing_view_name_errmsg = false
$scope.show_empty_errmsg = false

Initialize()
function Initialize()
{
    var grading_view = GetValue("grading-view")
    if (grading_view !== undefined)
        $scope.grading_view = grading_view
    var quiz_id = GetValue("quiz-id")
    InitializeAllQuestions(quiz_id)
}

function InitializeAllQuestions(quiz_id)
{
    $http.get("/quizzes/" + quiz_id + "/questions").then(function (resp) {
        $scope.all_questions = resp.data
    })
}

$scope.AddQuestionRow = function(grading_group)
{
    grading_group.questions.push({id: undefined, name: ""})
}

$scope.RemoveQuestionRow = function(grading_group, question)
{
    var i = grading_group.questions.indexOf(question)
    if (i > -1)
        grading_group.questions.splice(i, 1)
}
    
$scope.AddNewGradingGroup = function()
{
    var grading_group = {id: undefined, name: "", questions: []}
    $scope.grading_view.grading_groups.push(grading_group)
}


$scope.QuestionDropdownOnChange = function()
{
    $scope.available_questions = $scope.all_questions.filter(function(question) {
        return used_questions.indexOf(question) == -1
    })
}

$scope.Save = function()
{
    var is_valid_name = true
    var used_questions = []
    $scope.grading_view.grading_groups.forEach(function(grading_group) {
        grading_group.questions.forEach(function(q) { q.name = q.name.trim() })
        grading_group.questions = grading_group.questions.filter(function(q) { return q.name.length > 0 })
        used_questions = used_questions.concat(grading_group.questions)
        grading_group.name = grading_group.name.trim()
        is_valid_name = is_valid_name && grading_group.name.length > 0
    })

    var is_empty = $scope.grading_view.grading_groups.length == 0 
    var is_valid_questions = is_empty || used_questions.length > 0
    var seen = []
    for (var i =0; i < used_questions.length && is_valid_questions; i++) {
        var q = used_questions[i]
        if (seen.indexOf(q) == -1)
            seen.push(q)
        else
            is_valid_questions = false
    }

    $scope.grading_view.name = $scope.grading_view.name.trim()
    var is_valid_gv_name = $scope.grading_view.name.length > 0

    $scope.show_empty_errmsg = is_empty
    $scope.show_duplicate_questions_errmsg = !is_valid_questions
    $scope.show_invalid_name = !is_valid_name
    $scope.show_missing_view_name_errmsg = !is_valid_gv_name
    var is_valid = is_valid_questions && is_valid_name && is_valid_gv_name && !is_empty
    if (is_valid) {
        console.log("valid!")
    }
}

}) 

