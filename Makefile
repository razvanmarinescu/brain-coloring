all:
	configFile=config.py blender --background --python blendCreateSnapshot.py

convertToGif:
	cd output/DK_movie; ffmpeg -i cortical-outer_Image_%d.png -vf "fps=25,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0  cortical-outer.gif ; d cortical-outer.gif

# note: I tried GIF, but files end up with bad quality and large file size. Lossy compression with libx264 only allowed for mp4.
ffmpegConcatMovies:
	ffmpeg -i cortical-outer.gif -i cortical-inner.gif -i subcortical.gif -filter_complex "[0:v][1:v][2:v]hstack=inputs=3[v]" -map "[v]" -vf "scale=1920:820"  -codec:v libx264 -preset slow -crf 18 output_twitter.mp4

