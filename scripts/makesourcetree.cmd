SET batch_dir=%~dp0
SET output=source_tree.txt
@REM CMD /U /c tree %batch_dir%\..\ > sourcetree.txt
powershell -command "iex \"tree %batch_dir%\..\ /f\" > \"%output%\"