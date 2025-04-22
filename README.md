# html

```powershell
.\wget.exe --convert-links --page-requisites --adjust-extension --no-parent -P html_dir $URL
.\wget.exe --convert-links --page-requisites --adjust-extension --no-parent $URL
.\wget.exe `
  --convert-links `
  --page-requisites `
  --adjust-extension `
  --no-host-directories `
  --cut-dirs=100 `
  --directory-prefix=mypage `
  $URL
```
