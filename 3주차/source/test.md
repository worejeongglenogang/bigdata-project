$
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (master)
$ git remote add origin https://github.com/worejeongglenogang/bigdata-project.gi
t
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (master)
$ git branch -M main
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git push -u origin main
remote: Permission to worejeongglenogang/bigdata-project.git denied to kra2839.
fatal: unable to access 'https://github.com/worejeongglenogang/bigdata-project.git/': The requested URL returned error: 403
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cmdkey /delete:git:https://github.com

CMDKEY: 자격 증명을 삭제했습니다.
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git push -u origin main
info: please complete authentication in your browser...
Enumerating objects: 17043, done.
Counting objects: 100% (17043/17043), done.
Delta compression using up to 16 threads
Compressing objects: 100% (14822/14822), done.
Writing objects: 100% (17043/17043), 159.31 MiB | 17.99 MiB/s, done.
Total 17043 (delta 2049), reused 17043 (delta 2049), pack-reused 0 (from 0)     
remote: Resolving deltas: 100% (2049/2049), done.
To https://github.com/worejeongglenogang/bigdata-project.git
 * [new branch]        main -> main
branch 'main' set up to track 'origin/main'.
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git push -u origin main
branch 'main' set up to track 'origin/main'.
Everything up-to-date
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git add .
(venv) 
[main 178913e7] 테스트
 2 files changed, 1 insertion(+)
[main 178913e7] 테스트
 2 files changed, 1 insertion(+)
 create mode 100644 venv/xxx.py
(venv)
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git push origin main
Enumerating objects: 8, done.
Counting objects: 100% (8/8), done.
Delta compression using up to 16 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 614 bytes | 614.00 KiB/s, done.
Total 5 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/worejeongglenogang/bigdata-project.git
   9a566d66..178913e7  main -> main
(venv)
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ pwd
/c/Users/6-112/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ ls
app.py  requirements.txt  venv/
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ pwd; ls
/c/Users/6-112/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주
app.py  requirements.txt  venv/
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ .\venv\Scripts\Activate; python app.py
bash: .venvScriptsActivate: command not found
2026-03-20 14:48:53.221 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.221 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.463 
  Warning: to view this Streamlit app on a browser, run it with the following   
  command:

    streamlit run app.py [ARGUMENTS]
2026-03-20 14:48:53.463 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.464 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.464 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.464 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.464 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.465 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.465 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.465 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.465 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.465 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.465 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.467 Please replace `use_container_width` with `width`.      

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
2026-03-20 14:48:53.470 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.470 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.470 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.471 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.471 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.472 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.670 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.670 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.670 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.670 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.670 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.677 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.677 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.677 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.677 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.677 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.677 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.679 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.679 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-03-20 14:48:53.679 Session state does not function when running a script without `streamlit run`
2026-03-20 14:48:53.679 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.16.13.139:8501

2026-03-20 14:49:12.256 Please replace `use_container_width` with `width`.      

`use_container_width` will be removed after 2025-12-31.

For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
  Stopping...
(venv)
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ s
bash: s: command not found
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ ls
app.py  requirements.txt  venv/
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ dir
app.py  requirements.txt  venv
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ pwd
/c/Users/6-112/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git log --oneline
178913e7 (HEAD -> main, origin/main) 테스트
9a566d66 프로젝트 초기 설정
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git remote -v
origin  https://github.com/worejeongglenogang/bigdata-project.git (fetch)
origin  https://github.com/worejeongglenogang/bigdata-project.git (push)        
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git add .
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git commit -m "변경 내용 1"
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ git push
Everything up-to-date
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cd share
bash: cd: share: No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cd bigdata-project-b-전건주
bash: cd: bigdata-project-b-전건주: No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cd xxx.py
bash: cd: xxx.py: No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ mkdir mdfile
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cd mdfile
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ cd ..
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cat mdfile
cat: mdfile: Is a directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ ls mdfile
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cd mdfile
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ cat mdfile/README.md
cat: mdfile/README.md: No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ cd mdfile
bash: cd: mdfile: No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ touch test.md
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ ls
test.md
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ cat mdfile/test.md
cat: mdfile/test.md: No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ cat test.md
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ ls
test.md
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ mv  mdfile
mv: missing destination file operand after 'mdfile'
Try 'mv --help' for more information.
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ cd bigdata-project-b-전건주
bash: cd: bigdata-project-b-전건주: No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주/mdfile (main)
$ cd ..
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cd ..
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍
$ mv mdfile
mv: missing destination file operand after 'mdfile'
Try 'mv --help' for more information.
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍
$ mv mdfile my_folder
mv: cannot stat 'mdfile': No such file or directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍
$ cd bigdata-project-b-전건주
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ mv mdfile my_folder
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ mv mdfile 
mv: missing destination file operand after 'mdfile'
Try 'mv --help' for more information.
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ rm my_folder
rm: cannot remove 'my_folder': Is a directory
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ rm -r my_folder
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cp venv
cp: missing destination file operand after 'venv'
Try 'cp --help' for more information.
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cp -r venv
cp: missing destination file operand after 'venv'
Try 'cp --help' for more information.
(venv) 
6-112@112-20 MINGW64 ~/Desktop/빅데이터분석프로그래밍/bigdata-project-b-전건주 (main)
$ cp -r venv ..
(venv)