# Create release directory
$releaseDir = "release"
if (Test-Path $releaseDir) {
    Remove-Item -Recurse -Force $releaseDir
}
New-Item -ItemType Directory -Path $releaseDir | Out-Null

# Copy executable and required files
Copy-Item "dist\photo_finder.exe" -Destination $releaseDir
Copy-Item "README.md" -Destination $releaseDir

# Create a zip file
$version = "1.0.0"
$zipFile = "Photo_Finder_v$version.zip"
Compress-Archive -Path "$releaseDir\*" -DestinationPath $zipFile -Force

Write-Host "Release package created: $zipFile"
