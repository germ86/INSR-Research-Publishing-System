param(
  [switch]$StaticOnly,
  [switch]$Compile,
  [switch]$All
)
$ErrorActionPreference = "Stop"
if ($StaticOnly) {
  & bash ./tests/run-tests.sh --static-only
} elseif ($Compile -or $All) {
  & bash ./tests/run-tests.sh
} else {
  & bash ./tests/run-tests.sh
}
