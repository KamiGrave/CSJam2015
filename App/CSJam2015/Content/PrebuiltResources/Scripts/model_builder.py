#!/usr/bin/python
#
#  model_builder.py
#  CSJam2015
#  Created by Scott Downie on 30/06/2014.
#
#  The MIT License (MIT)
#
#  Copyright (c) 2014 Tag Games Limited
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#

import sys
import os
import subprocess
import shutil

#----------------------------------------
# @param the file path.
# @param the extension.
#
# @author Ian Copland
#
# @return whether or not the path has
# the extension.
#----------------------------------------
def HasExtension(filepath, extension):
    lower_filepath = filepath.lower()
    lower_extension = extension.lower()
    return lower_filepath.endswith(lower_extension)

#----------------------------------------
# Walks the input directory and converts
# all DAEs into csmodels
#
# @author S Downie
#
# @param Input path
# @param Output path
#----------------------------------------
def BuildModels(input_path, output_path):
	print("Building models...")

	if(input_path.endswith("/") == False):
		input_path = input_path + "/"

	if(output_path.endswith("/") == False):
		output_path = output_path + "/"

	for directory, sub_dirs, filenames in os.walk(input_path):
		input_dir = directory
		output_dir = os.path.join(output_path, input_dir[len(input_path):len(input_dir)]);

		if len(sub_dirs) == 0:
			for filename in filenames:
				if HasExtension(filename, ".dae") == True:
					if os.path.exists(output_dir) == False:
						os.makedirs(output_dir);

					BuildModel(os.path.join(directory, filename), os.path.join(output_dir, filename))

	print ("Model building finished")
	print("-----------------------------------------")
	print("-----------------------------------------")

#----------------------------------------
# Converts a single DAE to a csmodel
#
# @author S Downie
#
# @param Input path
# @param Output path
#----------------------------------------
def BuildModel(input_filepath, output_filepath):
	output_filename = os.path.splitext(output_filepath)[0]+".csmodel"
	print("Building model: " + output_filename)

	tool_path = os.path.join("..", "..", "ChilliSource", "Tools", "ColladaToCSModel.jar")

	subprocess.call(["java", "-Djava.awt.headless=true", "-Xmx512m", "-jar", tool_path, "--input", input_filepath, "--output", output_filename, "--swapyandz"]);

#----------------------------------------------------------------------
# The entry point into the script.
#
# @author S Downie
#
# @param The list of arguments.
#----------------------------------------------------------------------
def main(args):
	if not len(args) is 3:
		print("ERROR: Missing input and output paths")
		return

	input_path = args[1]
	output_path = args[2]

	if os.path.exists(output_path) == True:
		shutil.rmtree(output_path)

	BuildModels(input_path, output_path)

if __name__ == "__main__":
	main(sys.argv)

