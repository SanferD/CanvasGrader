var app = angular.module("grading-views", ["ngMaterial", "smart-table"])

app.controller("grading-views", function ($scope, $http) {

$scope.quiz_id = GetValue("quiz-id")
$scope.grading_view = {
    name: "",
    grading_groups: []
}
$scope.all_questions = []

$scope.show_errmsg_missing_view_name = false
$scope.show_errmsg_missing_groups = false
$scope.show_errmsg_missing_group_name = false
$scope.show_errmsg_missing_questions = false
$scope.show_errmsg_duplicate_questions = false

InitializePostHeaders($scope)
Initialize()
function Initialize()
{
    var grading_view = GetValue("grading-view")
    if (grading_view !== undefined)
        $scope.grading_view = grading_view
    InitializeAllQuestions()
}

function InitializeAllQuestions()
{
    $http.get("/quizzes/" + $scope.quiz_id + "/questions").then(function (resp) {
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
    RemoveEmptyQuestions()
    $scope.grading_view.name = $scope.grading_view.name.trim()
    var is_valid_view_name = $scope.grading_view.name.length > 0
    var has_grading_groups = $scope.grading_view.grading_groups.length > 0
    var has_valid_grading_group_names = true
    var has_questions_per_grading_group = true
    var has_no_duplicate_questions = true
    var seen = []
    $scope.grading_view.grading_groups.forEach(function(g) {
        g.name = g.name.trim()
        has_valid_grading_group_names = has_valid_grading_group_names && g.name.length > 0
        has_questions_per_grading_group = has_questions_per_grading_group && g.questions.length > 0

        for (var i = 0; i < g.questions.length && has_no_duplicate_questions; i++) {
            var q = g.questions[i]
            if (seen.indexOf(q) == -1)
                seen.push(q)
            else
                has_no_duplicate_questions = false
        }
    })

    $scope.show_errmsg_missing_view_name = !is_valid_view_name
    $scope.show_errmsg_missing_groups = !has_grading_groups
    $scope.show_errmsg_missing_group_name = !has_valid_grading_group_names
    $scope.show_errmsg_missing_questions = !has_questions_per_grading_group
    $scope.show_errmsg_duplicate_questions = !has_no_duplicate_questions

    var is_valid = is_valid_view_name && 
                   has_grading_groups && 
                   has_valid_grading_group_names && 
                   has_questions_per_grading_group && 
                   has_no_duplicate_questions
    if (is_valid) {
        console.log("valid!")
    }
}

function RemoveEmptyQuestions()
{
    $scope.grading_view.grading_groups.forEach(function(g) {
        g.questions = g.questions.filter(function(q) {
            return q.name.length > 0
        })
    })
}

}) 

