param (
    [Parameter(Mandatory=$true)]
    [string]$commitMessage
)

echo -----------------------GIT----------------------------

Import-Module -Name Posh-SSH

function Commit-And-Push($commitMessage) {
    # Run the test.py file
    python test.py

    # Check if the tests passed
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Tests failed. Changes not committed."
        return
    }

    # Add all changes to the Git repository
    git add .

    # Commit the changes with the specified message
    git commit -m $commitMessage

    # Push the changes to the remote repository
    git push
}

# Call the function with your commit message
Commit-And-Push $commitMessage

echo -----------------------FIN-GIT----------------------------

echo -----------------------FTP----------------------------
# Upload files to FTP server
$ftpServer = "10.8.0.10"
$userName = "waterleak"
$password = "waterleak"

$files = Get-ChildItem -Path . -Exclude venv -File

foreach ($file in $files) {
    $ftpPath = "ftp://$ftpServer/$file"
    $localPath = $file.FullName

    $ftpRequest = [System.Net.FtpWebRequest]::Create($ftpPath)
    $ftpRequest.Credentials = New-Object System.Net.NetworkCredential($userName, $password)
    $ftpRequest.Method = [System.Net.WebRequestMethods+Ftp]::UploadFile

    $fileContent = [System.IO.File]::ReadAllBytes($localPath)
    $ftpRequest.ContentLength = $fileContent.Length

    $ftpStream = $ftpRequest.GetRequestStream()
    $ftpStream.Write($fileContent, 0, $fileContent.Length)

    $ftpStream.Close()
}

Write-Host "Files uploaded successfully!"

echo -----------------------FIN-FTP----------------------------

echo -----------------------SSH--------------------------------
# SSH into remote Ubuntu server and replace IP address in files
$remoteServer = "10.8.0.10"
$userName = "waterleak"
$password = "waterleak"

$commands = @(
    'sudo pgrep -f "gunicorn -w 1 -b 10.8.0.10:8444 Prod_Profile_API:app" | sudo xargs kill',
    'sudo pgrep -f "gunicorn -w 1 -b 10.8.0.10:8445 Prod_Waterdata_API:app" | sudo xargs kill',
    'sudo pgrep -f "gunicorn -w 1 -b 10.8.0.10:8443 Prod_Login_API:app" | sudo xargs kill',
    'gunicorn -w 1 -b 10.8.0.10:8443 Prod_Login_API:app',
    'gunicorn -w 1 -b 10.8.0.10:8445 Prod_Waterdata_API:app',
    'gunicorn -w 1 -b 10.8.0.10:8444 Prod_Profile_API:app'
)

$session = New-SSHSession -ComputerName $remoteServer -Credential (New-Object System.Management.Automation.PSCredential ($userName, (ConvertTo-SecureString $password -AsPlainText -Force)))

Invoke-SSHCommand -SessionId $session.SessionId -Command "find /home/waterleak -type f -exec sed -i 's/10\.8\.0\.4/10.8.0.10/g' {} +"
foreach ($command in $commands) {
    Invoke-SSHCommand -SessionId $session.SessionId -Command $command
}


# Close SSH session
Remove-SSHSession -SessionId $session.SessionId