# Configure for your installation
$installPath = "$($env:LOCALAPPDATA)\Vivaldi\Application"

#  ==============================================================================
function Restore-Bundle {
  param ($path)
  Write-Host "* Restoring bundle.js from bundle.js.bak"
  Copy-Item "$path\bundle.js.bak" -Destination "$path\bundle.js"
}
function Backup-Bundle {
  param ($path)
  Write-Host "* Backing up current bundle.js as bundle.js.bak"
  Copy-Item "$path\bundle.js" -Destination "$path\bundle.js.bak"
}

function Wait-And-Exit {
  # If running in the console, wait for input before closing.
  if ($Host.Name -eq "ConsoleHost") {
    Write-Host "Press any key to EXIT..."
    $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyUp") > $null
    Exit
  }
}

function Parse-Bundle {
  param ($path)
  $parsedSections = @{}
  $data = Get-Content $path -Raw -Encoding utf8
  $data = $data -replace [regex]::Escape("(()=>{var e,t={")
  $data = $data.Substring(0, $data.IndexOf('},n={};function'))
  $data | Select-String -Pattern '(^|,)\d{1,6}:(\(|e).*?(?=(,\d{1,6}:(\(|e)|$))' -AllMatches |
  ForEach-Object {
    Write-Host $_.Matches[1].Groups[0].Value
  }
  # Write-Host $matches.groups[1].value
  # Set-Content -Path file2.json -Value $data
  # (^ | , )\d { 1, 6 }:\(.*?(?=(, \d { 1, 6 }:\( | $))
  # $sections = $data | ConvertFrom-Json
  # Write-Host $sections.76259

}


# find the path to the most recent version of Vivaldi
Get-ChildItem $installPath -Filter browser.html -Recurse | % { 
  $latestVersionFolder = $_.FullName -replace "\\browser.html", "" 
}

# make sure the path was found
if ($latestVersionFolder) {
  Write-Host "* Found latest version at: $latestVersionFolder"
}
else {
  Write-Warning "[Error] No instances of Vivaldi found at the provided install path: $installPath"
  Wait-And-Exit
}


# save a copy of the unedited file or follow user choice
if ((Test-Path "$latestVersionFolder\bundle.js.bak")) {
  Write-Warning "[Action Required] Backup of bundle.js found."
  Do {
    $answer = Read-host "Choose an option and enter the corresponding number:`
  - (1) [Recommended] Restore bundle.js from the backup and CONTINUE`
  - (2) Restore bundle.js from the backup and EXIT`
  - (3) Delete the backup and create a new one before CONTINUING`r`
Choice"
  }
  while ((1..3) -notcontains $answer )
}

switch ($answer) {
  1 {
    Restore-Bundle $latestVersionFolder
    Backup-Bundle $latestVersionFolder
  }
  2 {
    Restore-Bundle $latestVersionFolder
    Remove-Item -Path "$latestVersionFolder\bundle.js.bak"
    Wait-And-Exit
  }
  Default {
    Backup-Bundle $latestVersionFolder
  }
}

# load contents of bundle.js
$bundleJS = "$latestVersionFolder\bundle.js"

Parse-Bundle $bundleJS

# find the JSON hook files and implement the changes
Write-Host "* Starting to patch in hooks"
$scriptPath = Split-Path $MyInvocation.MyCommand.Path -Parent
Get-ChildItem $scriptPath -Filter *.json -Recurse | % { 
  $hookJson = Get-Content $_.FullName -Raw | ConvertFrom-Json
  $tempBundle = Get-Content $bundleJS -Raw -Encoding utf8

  Write-Host "---"
  Write-Host "* Patching in hook $_"
  
  $changeNumber = 0
  $saveChanges = $true
  ForEach ($change in $hookJson.replacements) {
    if (($change.find.Length -lt 2) -or ($change.replace.Length -lt 2)) {
      Write-Warning "[Invalid] Change number $changeNumber is invalid"
      $saveChanges = $false
      break
    }
    if ($tempBundle.Contains($change.find)) {
      Write-Host "** Made change number $changeNumber"
      Write-Host ([regex]::Escape($change.find))
      $tempBundle = $tempBundle.Replace($change.find, $change.replace)
      $changeNumber = $changeNumber + 1
    }
    else {
      Write-Warning "[Failure] Failed to find change number $changeNumber"
      $saveChanges = $false
      break
    }
  }

  # if changes were succefully made apply them to bundle.js
  if ($saveChanges) {
    Write-Host "** Saving changes to bundle.js"
    $tempBundle | Out-File $bundleJS -Encoding utf8
  }
  else {
    Write-Host "** Hook not applied to bundle.js"
  }
}

Write-Host "==="

Wait-And-Exit