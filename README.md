# jabra_csv_to_tcx_strava
Convert exported csv from jabra sports app to tcx files ready to upload to strava or endomondo.

#How to use  
1.Clone or download this repository  
2.Place both workout_summaries.csv and workout_updates in the same folder as the python files  
3.Execute the script: python jabra_csv_to_tcx_strava.py  
4.A TCX file will be created also in the same folder  

# Notes
If you live outside of the UTC timezone you may need to alter the from_timezone line at the top of
jabra_csv_to_tcx_strava.py in order to get accurate date/time stamps in the conversion.
