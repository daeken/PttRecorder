import wave, struct, sys
from glob import glob

def clean(samples):
	data = list(struct.unpack('<' + 'h' * (len(samples) / 2), samples))
	qr = min(len(data) / 10, 11025 * 2)
	for i in xrange(qr):
		data[i] = int(data[i] * (float(i) / (qr - 1)))
		data[-i - 1] = int(data[-i - 1] * (float(i) / (qr - 1)))
	return struct.pack('<' + 'h' * len(data), *data)

fns = reduce(lambda a, x: a + x, [sorted(glob('%s/*' % base)) for base in sys.argv[2:]], [])
data = [wav.readframes(wav.getnframes()) for wav in (wave.open(fn, 'rb') for fn in fns)]

out = wave.open(sys.argv[1], 'wb')
out.setnchannels(1)
out.setframerate(44100)
out.setsampwidth(2)
for i, elem in enumerate(data):
	out.writeframes(clean(elem))
	if i < len(data) - 1:
		out.writeframes('\0\0' * 22050)
