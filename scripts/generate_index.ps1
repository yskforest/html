$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$OutputFile = "index.html"
$HtmlHeader = @"
<html>
<head>
    <meta charset="UTF-8">
    <title>Index</title>
</head>
<body>
    <h1>HTML File List</h1>
    <ul>
"@

$HtmlFooter = @"
    </ul>
</body>
</html>
"@

$HtmlBody = ""

Get-ChildItem -Recurse -Filter *.html | ForEach-Object {
    $relPath = $_.FullName.Substring((Get-Location).Path.Length + 1).Replace('\', '/')
    $HtmlBody += "        <li><a href='$relPath'>$relPath</a></li>`n"
}

[System.IO.File]::WriteAllText($OutputFile, $HtmlHeader + $HtmlBody + $HtmlFooter, [System.Text.Encoding]::UTF8)

Write-Host "Done: index.html has been created."
