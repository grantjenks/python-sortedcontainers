@echo off
setlocal
set ITER=10000

del output.txt

call env26\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedlist %ITER% %%i >> output.txt 2>&1
call env26\Scripts\deactivate.bat

call env27\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedlist %ITER% %%i >> output.txt 2>&1
call env27\Scripts\deactivate.bat

call env32\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedlist %ITER% %%i >> output.txt 2>&1
call env32\Scripts\deactivate.bat

call env33\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedlist %ITER% %%i >> output.txt 2>&1
call env33\Scripts\deactivate.bat

call env26\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sorteddict %ITER% %%i >> output.txt 2>&1
call env26\Scripts\deactivate.bat

call env27\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sorteddict %ITER% %%i >> output.txt 2>&1
call env27\Scripts\deactivate.bat

call env32\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sorteddict %ITER% %%i >> output.txt 2>&1
call env32\Scripts\deactivate.bat

call env33\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sorteddict %ITER% %%i >> output.txt 2>&1
call env33\Scripts\deactivate.bat

call env26\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedset %ITER% %%i >> output.txt 2>&1
call env26\Scripts\deactivate.bat

call env27\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedset %ITER% %%i >> output.txt 2>&1
call env27\Scripts\deactivate.bat

call env32\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedset %ITER% %%i >> output.txt 2>&1
call env32\Scripts\deactivate.bat

call env33\Scripts\activate.bat
for /L %%i in (1 1 10) do python -m tests.test_stress_sortedset %ITER% %%i >> output.txt 2>&1
call env33\Scripts\deactivate.bat
