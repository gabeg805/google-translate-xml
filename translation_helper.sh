#!/bin/bash

# Directories
ANDROID_DIR=~/projects/android/app/NFCAlarmClock/app/src/main/res
TRANSLATION_DIR=~/projects/google_translate_xml

# File
file="$1"

# Language codes
lang="$2"
androidLang="$3"

# Android language omitted. Default it to the regular language code
if [ "${androidLang}" -eq "${androidLang}" ] 2> /dev/null
then
	echo ":: Android language defaulting to '${lang}'"
	androidLang="${lang}"
	shift
	shift

# Shift parameters so that starting parameter(s) are the line numbers
else
	shift
	shift
	shift
fi

androidFile="${ANDROID_DIR}/values-${androidLang}/${file}"
translationFile=$(ls -1 "${TRANSLATION_DIR}/${file%.*}"-* 2> /dev/null | grep -- "-${lang}" | head -1)

# Not enough arguments
if [ $# -eq 0 ]
then
	echo "Error: Not enough arguments."
	echo "./$(basename "$0") <file> <language code> [android regional language code] <line nums>...."
	exit 1

# Android file not found
elif [ ! -f "${androidFile}" ]
then
	echo "Error: Unable to find android file: '${androidFile}'"
	exit 2

# Translation file not found
elif [ ! -f "${translationFile}" ]
then
	echo "Error: Unable to find translation file. Available translations:"
	ls -1 "${TRANSLATION_DIR}/${file%.*}"-*
	exit 2

# Number of lines translated do not match the number that will be inserted into the android
# file (via the script arguments)
elif [ $(wc -l "${translationFile}" | cut -f 1 -d ' ') -ne $# ]
then
	echo "Error: Number of lines in the translation file ($(wc -l "${translationFile}" | cut -f 1 -d ' ')) do not match the number of line numbers passed to this script ($#)"
	exit 3
fi

echo ":: File               : $file"
echo ":: Language code      : $lang"
echo ":: Android lang. code : $androidLang"

# Backup resources to /tmp
echo ":: Backing up file that will be modified"
cp -avf "${androidFile}" /tmp

# Read the translation file, line by line
args=("$@")
i=0
while IFS= read -r line
do

	# Get line at line number
	#line=$(sed "${n}!d" ${translationFile})

	# Get line number to change
	num=${args[$i]}
	i=$[ $i + 1 ]

	# Escape special characters in line
	escapedLine=$(printf "%s\n" "$line" | sed -e 's/\&/\\\&/g' -e 's/\;/\\\;/g' -e "s/'/\\\'/g")
	#echo -e "$line"
	#echo -e "$escapedLine"
	#echo

	# Insert line into android file at line number
	# Note: This command looks weird but is needed so that \t tab characters are interpretted
	#       correctly
	sed -i $"${num}i\\
$escapedLine" "${androidFile}"

done < "${translationFile}"

