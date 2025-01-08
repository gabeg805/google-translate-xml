# 
# NAME
#     google_translate_xml.py
# 
# SYNOPSIS
#     python3 google_translate_xml.py
# 
# DESCRIPTION
#     Use Google's Translation API to translate an XML file.
#     
#     This has been primarily tested on XML files that are used in Android
#     development (arrays.xml, strings.xml, etc.)
#     
#     Note: This translation is slow (~1 translation / sec) due to just
#           focusing on keeping the logic straightforward, and to that end, it
#           allows for preserving the format of the original file, which was
#           one of the primary interests outside of being able to translate a
#           file.
# 

import argparse
import os
import re
import sys
from google.cloud import translate_v3

# Create the parser
parser = argparse.ArgumentParser(
	prog=os.path.basename(sys.argv[0]),
	description="Parse an XML file, such as strings.xml for an Android app, and translate each item in the file.  This uses the Google Translation API so you need to have an API key to use this script.  The process can be a little slow because it queries each item line by line, but you can see the output and catch any potential failures, and the structure of your original file is copied in the output file.")

# Add arguments to the parser
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-f", "--file", help="The XML file to translate.")
group.add_argument("-t", "--text", help="The text to translate.")
parser.add_argument("-l", "--language", required=True, help="The ISO 639-1 code of the language to translate the file to. See header of script for where to find full list of available languages.")
parser.add_argument("-o", "--output", help="The output file where the translation will be written to.")
parser.add_argument("-p", "--project", help="The Google Cloud Project ID")

# Parse the arguments
args = parser.parse_args()

# Define globals
XML_FILE = args.file
TEXT = args.text
LANGUAGE = args.language
OUTPUT_FILE = args.output if args.output else f"{XML_FILE}-{LANGUAGE}"
PROJECT_ID = args.project if args.project else os.environ.get("GOOGLE_CLOUD_PROJECT")

# Check if file exists
if XML_FILE is not None and not os.path.isfile(XML_FILE):
	print(f"Error: XML file was not found '{XML_FILE}'")
	exit(1)

# Check if text is not empty
if TEXT is not None and not TEXT:
	print(f"Error: Text was not found '{TEXT}'")
	exit(1)

# Check the project ID
if not PROJECT_ID:
	print("Error: Must specify a project ID either as an argument or must be an environment variable that you have set.")
	exit (1)

# Initialize Translation client
def translate_text(
	text: str = "Hello please translate this",
	language_code: str = "de",
) -> translate_v3.TranslationServiceClient:
	"""
	Translating Text from English.

	Args:
		text: The content to translate.
		language_code: The language code for the translation.
			E.g. "fr" for French, "es" for Spanish, etc.
			Available languages: https://cloud.google.com/translate/docs/languages#neural_machine_translation_model
	"""

	client = translate_v3.TranslationServiceClient()
	parent = f"projects/{PROJECT_ID}/locations/global"
	# Translate text from English to chosen language
	# Supported mime types: # https://cloud.google.com/translate/docs/supported-formats
	response = client.translate_text(
		contents=[text],
		target_language_code=language_code,
		parent=parent,
		mime_type="text/plain",
		source_language_code="en-US",
	)

	# Display the translation for each input text provided
	#for translation in response.translations:
	#	print(f"Translated text: {translation.translated_text}")

	# Return the translated text
	if response.translations:
		return response.translations[0].translated_text 

	# No translation found. Return an empy string
	else:
		return ""

# Translate file
if XML_FILE:

	# Write to other file
	with open(OUTPUT_FILE, "w") as writeStream:

		# Reading file
		with open(XML_FILE, "r") as readStream:

			# Iterate over each line in the file
			for i,line in enumerate(readStream):

				# Strip whitespace from line
				stripline = line.strip()

				# String
				if stripline.startswith("<string "):
					match = re.findall(r"<string.*?>(.*?)</string>", stripline, re.DOTALL)

				# Item
				elif stripline.startswith("<item"):
					match = re.findall(r"<item.*?>(.*?)</item>", stripline, re.DOTALL)

				# Regular line. Just write it to the output file
				else:
					writeStream.write(line)
					continue

				# Make sure a match was found
				if not match:
					continue

				# Check if the match has a reference to another tag
				if match[0].startswith("@"):
					writeStream.write(line)
					continue

				# Log the match
				print(repr(match[0]))

				# Translate the line
				translation = translate_text(match[0], language_code=LANGUAGE)

				# Log the translation
				print(repr(translation))
				print("")

				# Write the translation to the file
				writeStream.write(line.replace(f">{match[0]}<", f">{translation}<"))

# Translate text
elif TEXT:

	# Log the text
	print(repr(TEXT))

	# Translate the line
	translation = translate_text(TEXT, language_code=LANGUAGE)

	# Log the translation
	print(repr(translation))
	print("")

