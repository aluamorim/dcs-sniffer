

echo "Converting UI design file..."
pyuic5 ./py/mainwindow.ui -o ./py/maindesign.py -x
pyuic5 ./py/adcdialog.ui -o ./py/adcdialog.py -x
pyuic5 ./py/waveformgen.ui -o ./py/modules/dialog/tonedesign.py -x
echo "MainUIWindow class generated."

