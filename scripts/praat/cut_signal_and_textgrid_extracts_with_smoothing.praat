# cut_signal_and_textgrid_extracts_with_smoothing.praat
#
# Cut a set of sounds paired with textgrid files, and add leading and trailing silence.
# Sounds are cut according to the position of specific intervals in the textgrid
# (from the start of startIntervalLabel to the end of endIntervalLabel).
# If the same label is used in several intervals, the first one is retained.
# A fade in and fade out is applied before and after the cutting points.
#
# Author: Nicolas Audibert, LPP UMR7018, October 2017
form cut_signal_and_textgrid_extracts_with_smoothing
	sentence sndFilesFolder /Users/nicolasaudibert/Documents/LPP/hesitation_NCCFr/annotation_hesitation_NCCFr/wav
	sentence textgridFilesFolder /Users/nicolasaudibert/Documents/LPP/hesitation_NCCFr/annotation_hesitation_NCCFr/TextGrid_NCCFr_annotations_posttraitees
	sentence sndFilesOutFolder extraitsDecoupes
	sentence textgridFilesOutFolder extraitsDecoupes
	word textgridsSuffix 
	word wavSuffix 
	word textgridsExtension .TextGrid
	word wavExtension .wav
	positive targetTierIndex 6
	boolean extractAllNonEmptyIntervals 1
	# the following parameter is used only if extractAllNonEmptyIntervals is set to 0 (False)
	sentence regexTargetIntervals [^\s]+
	boolean use_interval_labels_in_extracts_names 0
	word extracts_file_names_base_string extrait
	sentence extracts_list_filename reference_extraits.txt
	real leadingSilenceDuration 0.1
	real smoothedPartDurationBefore 0.005
	real trailingSilenceDuration 0.1
	real smoothedPartDurationAfter 0.005
endform

# Clean out the info window
clearinfo

# Get the list of textgrids in the specified folder that match the regular expression
textgridsFolderRegex$ = textgridFilesFolder$+ "/*" + textgridsSuffix$ + textgridsExtension$
filesList = Create Strings as file list: "fileslist", textgridsFolderRegex$
nfiles = Get number of strings

# Create the target directories if needed (commands ignored if directories already exist)
createDirectory: sndFilesOutFolder$
createDirectory: textgridFilesOutFolder$

# Write the header of the extracts reference file
writeFileLine: extracts_list_filename$, "original_textgrid_file", tab$, "original_wav_file", tab$, "extract_sound_file_name", tab$, "extract_textgrid_file_name", tab$, "extract_start_time_in_original_file", tab$, "extract_end_time_in_original_file", tab$, "interval_label_in_original_file"

# Loop every nfiles textgrid
for ifile to nfiles
	# Read the textgrid and the sound
	selectObject: filesList
	currentTG$ = Get string: ifile
	currentTGpath$ = textgridFilesFolder$ + "/" + currentTG$
	currentFileBasename$ = currentTG$ - textgridsExtension$ - textgridsSuffix$
	currentSnd$ = currentFileBasename$ + wavSuffix$ + wavExtension$
	currentSndPath$ = sndFilesFolder$+ "/" + currentSnd$

	appendInfo: currentFileBasename$

	tg = Read from file: currentTGpath$
	snd = Open long sound file: currentSndPath$

	# Loop all intervals to find the matching ones
	selectObject: tg
	nInterv = Get number of intervals: targetTierIndex
	# Counter for extracts indices
	iExtract = 0
	for iInterv from 1 to nInterv
		# Check if the current interval matches the regular expression
		selectObject: tg
		currentIntervLabel$ = Get label of interval: targetTierIndex, iInterv
		# Check that the current interval is not empty
		if currentIntervLabel$<>""
			# If only intervals matching the regex are to be extracted, check it
			if extractAllNonEmptyIntervals or index_regex(currentIntervLabel$, regexTargetIntervals$)>0
				# It's a target interval: get its start and end points
				extractionStartTime = Get start time of interval: targetTierIndex, iInterv
				extractionEndTime = Get end time of interval: targetTierIndex, iInterv

				# Get the name of the extract
				iExtract = iExtract + 1
				currentExtractBasename$ = currentFileBasename$ + "_" + extracts_file_names_base_string$ + fixed$(iExtract, 0)
				if use_interval_labels_in_extracts_names
					currentExtractBasename$ = currentExtractBasename$ + "_" + currentIntervLabel$
				endif
	
				# Cut the textgrid object according to the start and end points of the target intervals
				selectObject: tg
				cutTextgrid = Extract part: extractionStartTime, extractionEndTime, "no"
				# Add the time corresponding to the silent parts
				Extend time: leadingSilenceDuration, "Start"
				Shift times by: leadingSilenceDuration
				Extend time: trailingSilenceDuration, "End"
				tgExtractTotalDuration = Get total duration

				# Save the modified textgrid to file
				currentTGPathOut$ = textgridFilesOutFolder$+ "/" + currentExtractBasename$ + textgridsExtension$
				Write to text file: currentTGPathOut$

				# Get the sampling frequency and duration of the original signal
				selectObject: snd
				fs = Get sampling frequency
				sndDuration = Get total duration

				# Create the silence to be inserted before the cut part
				if leadingSilenceDuration-smoothedPartDurationBefore>0
					silenceBefore = Create Sound from formula: "silence", 1, 0, leadingSilenceDuration-smoothedPartDurationBefore, fs, "0"
				endif

				# Cut the sound object, keeping the part to be smoothed before and after
				selectObject: snd
				sndExtract = Extract part: extractionStartTime-smoothedPartDurationBefore, extractionEndTime+smoothedPartDurationAfter, "no"
				sndExtractDuration = Get total duration

				# Apply a fade in to the part to be smoothed before the target part
				if smoothedPartDurationBefore>0
					selectObject: sndExtract
					Fade in: 0, 0, smoothedPartDurationBefore, "yes"
				endif
				# Apply a fade out to the part to be smoothed after the target part
				if smoothedPartDurationAfter>0
					selectObject: sndExtract
					Fade out: 0, sndExtractDuration, -smoothedPartDurationAfter, "yes"
				endif

				# Create the silence to be inserted after the cut part
				if trailingSilenceDuration-smoothedPartDurationAfter>0
					silenceAfter = Create Sound from formula: "silence", 1, 0, trailingSilenceDuration-smoothedPartDurationAfter, fs, "0"
				endif

				# Add silence before and after the sound extract
				if leadingSilenceDuration-smoothedPartDurationBefore>0 and trailingSilenceDuration-smoothedPartDurationAfter>0
					selectObject: silenceBefore
					plusObject: sndExtract
					plusObject: silenceAfter
					processedSnd = Concatenate
					removeObject: silenceBefore, silenceAfter
				elsif leadingSilenceDuration-smoothedPartDurationBefore>0
					selectObject: silenceBefore
					plusObject: sndExtract
					processedSnd = Concatenate
					removeObject: silenceBefore
				elsif trailingSilenceDuration-smoothedPartDurationAfter>0
						selectObject: sndExtract
						plusObject: silenceAfter
						processedSnd = Concatenate
						removeObject: silenceAfter
				else
						selectObject: sndExtract
						processedSnd = Copy
				endif

				# Save the extracted sound to file
				selectObject : processedSnd
				sndExtractTotalDuration = Get total duration
				currentSndPathOut$ = sndFilesOutFolder$+ "/" + currentExtractBasename$ + wavExtension$
				Write to WAV file: currentSndPathOut$
				removeObject: sndExtract, processedSnd, cutTextgrid

				# Export current extract info the text file
				appendFileLine: extracts_list_filename$, currentTG$, tab$, currentSnd$, tab$, currentExtractBasename$ + wavExtension$, tab$, currentExtractBasename$ + textgridsExtension$, tab$, extractionStartTime, tab$, extractionEndTime, tab$, currentIntervLabel$

				# Check that Sound and TextGrid extract duration match (possible discrepancy due to rounding errors, but should be less than 1 millisecond)
				if abs(sndExtractTotalDuration-tgExtractTotalDuration)>=0.001
					appendInfoLine: tab$, "Duration mismatch for extract ", currentExtractBasename$, ": sound duration = ", sndExtractTotalDuration, " s, textgrid duration = ", tgExtractTotalDuration, " s"
				endif
			endif
		endif
	endfor
	appendInfoLine: "... ", iExtract, " extracts"
	removeObject: tg, snd
endfor

removeObject: filesList
