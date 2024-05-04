import os
import subprocess
import sys
from io import BufferedReader

subprocessStartUpInfo = subprocess.STARTUPINFO()
subprocessStartUpInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
subprocessStartUpInfo.wShowWindow = subprocess.SW_HIDE

ytdlp_file_path = "./external/ytdlp/yt-dlp.exe"
ffmpeg_file_path = "./external/ffmpeg/ffmpeg.exe"
args = ["--version"]
os.chdir(sys.path[0])
print(sys.path[0])
# process = subprocess.Popen(f"{exe_file_path} {' '.join(args)}", shell=True)
# subprocess.run([absolute_exe_path] + args, cwd=directory, shell=True, check=True)
# process = subprocess.Popen([absolute_exe_path] + args, cwd=directory, shell=True)
process = subprocess.Popen(
    sys.path[0] + f"{ffmpeg_file_path} {' '.join(args)}",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    startupinfo=subprocessStartUpInfo,
)


stdout = BufferedReader(process.stdout.raw)
while True:
    line = stdout.readline()
    if not line:
        break
    try:
        print(line.decode("utf-8"), end="")
    except UnicodeDecodeError:
        print(line.decode("gbk"), end="")
# stdout, stderr = process.communicate()
# exit_code = process.returncode
#
# print(f"STDOUT: {stdout.decode()} STDERR: {stderr.decode()}")
