
cd repo\aima-python
if  errorlevel 1 goto ERROR
pip install -r requirements.txt
if  errorlevel 1 goto ERROR
git submodule init
if  errorlevel 1 goto ERROR
git submodule update
if  errorlevel 1 goto ERROR
pip install pytest
if  errorlevel 1 goto ERROR
py.test
if  errorlevel 1 goto ERROR
goto EOF

:ERROR
echo Failed
cmd /k
exit /b 1

:EOF 
echo "Instalation OK"
exit /b 0