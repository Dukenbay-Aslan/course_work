# path_to_wav|text|text|duration.xx
import librosa as lr
import numpy as np
import os

def trim(start, finish, wav_from, wav_to):
	start = start * 100
	start = int(start)
	start = start / 100
	mins = start // 60
	mins = int(mins)
	secs = start - mins*60

	finish = finish * 100
	finish = int(finish)
	finish = finish / 100
	minf = finish // 60
	minf = int(minf)
	secf = finish - minf*60
	
	command = f"ffmpeg -ss 00:{mins}:{secs} -to 00:{minf}:{secf} -i {wav_from} {wav_to}"
	os.system(command)

def hmwords(tence):
	words = tence.split()
	for word in words:
		if word == "–":
			words.remove(word)
	return len(words)

def tcwc(name, txt_path):
	wav_path = txt_path.replace("txt", "wav")
	f = open(txt_path, 'r')
	tences = f.readline().split('.')
	f.close()

	l = len(tences)
	i = 0
	while (i < l):
		if len(tences[i]) < 3:
			del tences[i]
			i = i - 1
			l = l - 1
		i = i + 1
	tc = len(tences)

	transcript = open("datas/trancript.txt", 'w')

	mu = 0.5572950206058496
	amplitudes, sfreq = lr.load(wav_path)
	time = np.arange(0, len(amplitudes)) / sfreq
	l = len(time)
	longness = l // 20
	ind = 0
	for j in range(tc):
		wav_to = "datas/abay_joly/" + name
		if j < 9:
			wav_to = wav_to + "_0000"
		elif (j >= 9) & (j < 99):
			wav_to = wav_to + "_000"
		elif (j >= 99) & (j < 999):
			wav_to = wav_to + "_00"
		elif (j >= 999) & (j < 9999):
			wav_to = wav_to + "_0"
		else:
			wav_to = wav_to + "_"
		wav_to = wav_to + str(j + 1) + ".wav"
		wc = hmwords(tences[j])
		t = wc * mu
		k = 0
		start = 0
		finish = mu
		duration = finish - start
		i = ind
		while (i < ind + longness) & (i < l):
			if ((abs(amplitudes[i]) != 0.0) & (abs(amplitudes[i]) < 1.7e-6)):
				start = finish
				finish = time[i]
				if (abs(time[i] - t) < mu):
					duration = finish - start
					ind = i
					trim(start, finish, wav_path, wav_to)
					transcript.write(wav_to)
					transcript.write('|')
					transcript.write(tences[j])
					transcript.write('|')
					transcript.write(tences[j])
					transcript.write('|')
					transcript.write(str(duration))
					transcript.write('\n')
					break
			i = i + 1
	transcript.close()

file = open("attary.txt", 'r')
for txt in file:
	sz = len(txt)
	txt = txt[0:sz-1]
	txt_path = "path_to_dataset/" + txt + ".txt"
	print(f"\t\tWorking with {txt_path}")
	tcwc(txt, txt_path)
file.close()
