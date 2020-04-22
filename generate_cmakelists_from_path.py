#!/usr/bin/python3

import glob
import subprocess

ignore_path = ["cmake-build-debug"] # folder you want to ignore
cmakelists_path = "CMakeLists.txt"

def run_bash_cmd(cmd):
    output = None
    try:
        output = subprocess.check_output(cmd, shell=True).decode('UTF-8').strip()
    except:
        print("exit 1")
    return output

def isPathInIgnoreList(path):
    match = False
    for ignore in ignore_path:
        if (ignore in path):
            match = True
    return match

def find_files(path, files_found):
    for filename in glob.iglob(path, recursive=True):
        filename_fixed = filename.replace('\\', '/')
        base = filename_fixed.split("/")
        base.pop(0)
        base.pop(0)
        filename_edited = "/".join(base)
        if (not isPathInIgnoreList(filename_edited)):
            files_found.append(filename_edited)
            print("  filename: " + filename)
            print("    edited: ./" + filename_edited)

def find_folders(files_found):
    folders_found = []
    for f in files_found:
        base = f.split("/")
        base.pop()
        path_edited = "/".join(base)
        if (not isPathInIgnoreList(path_edited)):
            folders_found.append(path_edited)
    folders_found = list(set(folders_found))
    return(folders_found)

def get_project_folder_name():
    cmd = "pwd"
    output = run_bash_cmd(cmd)
    return output.split('/')[-1]

if __name__ == "__main__":
    print("##### GENERATE_MAKEFILESOURCE #####")
    print()

    files_found = []
    folders_found = []

    print("##### found source files #####")
    find_files('./**/*.c', files_found)
    find_files('./**/*.cpp', files_found)
    files_found.sort()
    print()

    print("##### found source include folders #####")
    folders_found = find_folders(files_found)
    for f in folders_found:
        print("  folder: ./" + f)
    print()

    cmakelists_file = open(cmakelists_path, 'w')

    project_folder_name = get_project_folder_name()

    cmakelists_file.write("cmake_minimum_required(VERSION 3.10)\n")
    cmakelists_file.write("project(" + project_folder_name + ")\n")

    cmakelists_file.write("include_directories(\n")
    for line in folders_found:
        cmakelists_file.write("    ./" + line + "\n")
    cmakelists_file.write(")\n")

    cmakelists_file.write("add_executable(src\n")
    for line in files_found:
        cmakelists_file.write("    ./" + line + "\n")
    cmakelists_file.write(")\n")

    print("Yes.")
