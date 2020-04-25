function GetValue(id)
{
    var value = document.getElementById(id).value
    if (value == "None")
        value = undefined
    return value
}

function GetValueJSON(id)
{
    var value = GetValue(id)
    value = value.replace(/'/g, '"')
    value = value.replace(/None/g, null)
    value = value.replace(/True/g, true)
    value = value.replace(/False/g, false)
    return JSON.parse(value)
}

function ParseCookies(cookie)
{
    var cookies = {}
    var split = cookie.split(";")
    for (var i = 0; i < split.length; i++) {
        value = split[i]
        value_split = value.split("=")
        cookies[value_split[0]] = value_split[1]
    }
    return cookies
} 

function InitializePostHeaders($scope)
{
    $scope.cookies = ParseCookies(document.cookie)
    $scope.post_headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": $scope.cookies.csrftoken
    }
}

function GetIndeces(length)
{
    var A = []
    for (var i = 0; i < length; i++)
        A.push(i)
    return A
}

function IsNumber(s) {
    return !isNaN(s)
}

function BuildRequirements(validators)
{
    return validators.map(function(requirement) {
        return new Requirement(requirement[0], requirement[1])
    })
}

function Requirement(requirement, validate)
{
    this.text = requirement
    this.is_met = false
    this.validate = validate
}

