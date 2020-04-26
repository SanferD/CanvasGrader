var app = angular.module("grader", ["ngMaterial", "smart-table"])

app.controller("grader", function ($scope, $http) {
    InitializeGraderAPI($scope, $http)
    InitializeGrader($scope, $http)
})

