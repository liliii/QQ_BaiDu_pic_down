@ECHO OFF
REM �����ӳ�
SETLOCAL ENABLEDELAYEDEXPANSION

REM File List
SET LIST=Yphone.txt
 
REM Log File
SET LOG=exec.log

REM Get file list
IF EXIST "%LIST%" (
   del %LIST%  >> %LOG%
 )
dir/b/o-d/a *.jpg >> %LIST%

FOR /F "tokens=1,2 delims=."  %%a IN (%LIST%) DO (
 
   SET /a x=!x!+1
   SET nm=00000!x!

   REM file rename
   ren %%a.%%b Yphone!nm:~-8!.jpg
   ECHO ren %%a.%%b Yphone!nm:~-8!.jpg >> %LOG%
 
 )

28 ECHO Success!!! >> %LOG%