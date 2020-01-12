form extract_non_silent_parts_from_sound_files
	sentence inputSndFilesFolder /home/wran/plurital/voice-language-recognizer/data/1_snd
	word inputSndFilesExtension .wav
	word inputSndFilesRegex *.wav
	sentence outputSndFilesFolder /home/wran/plurital/voice-language-recognizer/data/2_rmv_silence
	word outputSndFilesSuffix _sans_silence
	# non-silent parts detection settings
	positive minF0_Hz 75
	comment Silence treshold (energy difference between non-silent and silent parts, in dB)
	positive silenceTreshold_dB 25
	real minimumSilentIntervalDuration_seconds 0.05
	real minimumNonSilentIntervalDuration_seconds 0.05
endform

# Create target folder if needed
createDirectory: outputSndFilesFolder$

# Get the list of sound files to be processed
sndFilesSearchPath$ = inputSndFilesFolder$ + "/" + inputSndFilesRegex$
fileslist = Create Strings as file list: "fileslist", sndFilesSearchPath$
nFiles = Get number of strings

for iFile from 1 to nFiles
	# Read the sound file
	selectObject: fileslist
	currentSndFile$ = Get string: iFile
	currentSndFileBasename$ = currentSndFile$ - inputSndFilesExtension$
	currentSnd = Read from file: inputSndFilesFolder$ + "/" + currentSndFile$

	selectObject: currentSnd
	# Get the segmentation in silent and non-silent parts in a new TextGrid
	currentSilenceNonsilenceTextGrid = To TextGrid (silences): minF0_Hz, 0, -silenceTreshold_dB, minimumSilentIntervalDuration_seconds, minimumNonSilentIntervalDuration_seconds, "", "nonsilent"

	# Extract all parts considered as non-silent as separate Sound objects
	selectObject: currentSnd
	plusObject: currentSilenceNonsilenceTextGrid
	Extract intervals where: 1, "no", "is equal to", "nonsilent"

	# Check that non silent parts were extracted
	nNonSilentParts = numberOfSelected()
	if nNonSilentParts > 0
		# Store corresponding references in an array
		for i from 1 to nNonSilentParts
			nonSilentPart[i] = selected(i)
		endfor

		# Concatenate all non silent parts (still selected)
		concatenatedNonSilentParts = Concatenate

		# Save concatenated non silent parts
		currentSndOutPath$ = outputSndFilesFolder$ + "/" + currentSndFileBasename$ + outputSndFilesSuffix$ + ".wav"
		selectObject: concatenatedNonSilentParts
		Save as WAV file: currentSndOutPath$

		# Clean-up: remove non silent parts and concatenated version
		for i from 1 to nNonSilentParts
			removeObject: nonSilentPart[i]
		endfor
		removeObject: concatenatedNonSilentParts
	endif

	# Clean-up: remove remaining temporary objects
	removeObject: currentSilenceNonsilenceTextGrid, currentSnd
endfor

# Clean-up: remove the list of sound files
removeObject: fileslist

writeInfoLine: "Extracted non silent parts from ", nFiles, " files into folder ", outputSndFilesFolder$
