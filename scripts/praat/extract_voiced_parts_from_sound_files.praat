form extract_voiced_parts_from_sound_files
	sentence inputSndFilesFolder extraits_audio
	word inputSndFilesExtension .wav
	word inputSndFilesRegex *.wav
	sentence outputSndFilesFolder extraits_audio/partie_voisee
	word outputSndFilesSuffix _voise
	# F0 detection settings
	positive minF0_Hz 75
	positive maxF0_Hz 600
	# Voiced parts detection settings
	real maxPeriodDuration_seconds 0.02
	real meanPeriodDuration_seconds 0.01
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
	# Get the f0 contour
	f0 = To Pitch: 0, minF0_Hz, maxF0_Hz
	# Derive a PointProcess (= glottis closure instants) from the f0 detection
	pp = To PointProcess
	# Convert it to a TextGrid (annotation grid) with parts considered as voiced or unvoiced
	currentVUVtextGrid = To TextGrid (vuv): maxPeriodDuration_seconds, meanPeriodDuration_seconds

	# Extract all parts considered as voiced as separate Sound objects
	selectObject: currentSnd
	plusObject: currentVUVtextGrid
	Extract intervals where: 1, "no", "is equal to", "V"

	# Check that voiced parts were extracted
	nVoicedParts = numberOfSelected()
	if nVoicedParts > 0
		# Store corresponding references in an array
		for i from 1 to nVoicedParts
			voicedPart[i] = selected(i)
		endfor

		# Concatenate all voiced parts (still selected)
		concatenatedVoicedParts = Concatenate

		# Save concatenated voiced parts
		currentSndOutPath$ = outputSndFilesFolder$ + "/" + currentSndFileBasename$ + outputSndFilesSuffix$ + ".wav"
		selectObject: concatenatedVoicedParts
		Save as WAV file: currentSndOutPath$

		# Clean-up: remove voiced parts and concatenated version
		for i from 1 to nVoicedParts
			removeObject: voicedPart[i]
		endfor
		removeObject: concatenatedVoicedParts
	endif

	# Clean-up: remove remaining temporary objects
	removeObject: f0, pp, currentVUVtextGrid, currentSnd
endfor

# Clean-up: remove the list of sound files
removeObject: fileslist

writeInfoLine: "Extracted voiced parts from ", nFiles, " files into folder ", outputSndFilesFolder$
