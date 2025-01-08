# Google Translate XML
Use Google's Translation API to translate an XML file.

# Prerequisites
1. Create a Google Cloud account. (This is free)

2. Create a project in your account. **Note the Project ID, you will need this
   later**.

3. Enable the Translation API.

   If you do not do this now, it is OK. Just know that you will get an error
   when you try to run the script saying something about how the API may not be
   enabled yet, and there will be a link directing you to enable it. You can
   put this off if you just want to wait for that error to get the link.

4. Install the Google Cloud CLI.

   `https://cloud.google.com/sdk/docs/install`

5. Source the Google Cloud environment, or logout and log back into your
   machine to have your shell source it for you:

   `. /etc/profile.d/google-cloud-cli.sh`

6. Install the Google Cloud Translation API in a virtual environment.

   `python3 -m venv <YOUR-ENV>
   source <YOUR-ENV>/bin/activate
   pip install google-cloud-translate`

   Where **<YOUR-ENV>** is a name of your choosing.

7. Initialize the Google Cloud CLI:

   `gcloud init`

8. Create local authentication credentials for your user account:

   `gcloud auth application-default login`

9. Try to run this script.

# Examples

## Translate from English to German.

`python3 google_translate_xml.py -f strings.xml -l de -p <PROJECT_ID>`

Where **<PROJECT_ID>** is your project ID. This can be found in your Google Cloud
Console.

## Translate from English to German without Specifying Project ID

You can set the `GOOGLE_CLOUD_PROJECT` environment variable with your project
ID so that you do not have to keep using the `-p` flag.

`export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>`

Where **<PROJECT_ID>** is your project ID. Then run the script without the -p
flag.

`python3 google_translate_xml.py -f strings.xml -l de`

# Notes
The list of available languages to translate to can be found here:

<https://cloud.google.com/translate/docs/languages#neural_machine_translation_model>
