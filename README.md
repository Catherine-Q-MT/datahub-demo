# Datahub Demo

This is a basic demo repo to showcase different ways of using datahub. It was built looking at Version 0.10.0

To use it:
* Have Docker Desktop installed on your machine
* in the command line activate the python env
* Check the recipe cards and code and change to storage relevent to you (i.e your own S3 resources for example)
* Export secrets and keys accordingly 
* Run the 'nuke everything and start again script' OR cherry pick commands from it. If you run it it will nuke your docker and the run an install of the quick start datahub (which will run on local host 9002). I did this as I noticed there were issues when I tried to tear down and re-run infrastructure. this script will scrub everything and restart the server. 
* To run the recipe cards you can trigger the run_ingestion script from the datahub demo dir or if you look at the script you should be able to infer how to run the cards individually
* Run the python as per normal 

What this is:
* An investigation into the SDK of datahub and its data model

What this is not:
* A demonstration of best practice when writing scripts using the SDK
* The 'correct' way of using the SDK

Known Issues:
Spark Lineage and consumption from the Jupyter notebook did not work as expected 
