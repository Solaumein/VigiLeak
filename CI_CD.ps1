param (
    [Parameter(Mandatory=$true)]
    [string]$commitMessage
)

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
