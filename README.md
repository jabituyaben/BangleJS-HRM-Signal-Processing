# BangleJS-HRM-Signal-Processing

Python implementation of signal processing to extract HRV metrics from Bangle.JS raw HRM data. Uses scipy and hrvanalysis.

In the same folder as the script, you need to keep a CSV file of extracted readings from the hrm.raw element of the Heat rate data object from the HR event on the Bangle.JS. I've written a companion app to extract this, which is uploaded here for now but will also be in the Bangle App Loader and maintained better there. The signal_processing script could also be adapted to work with other sensor readings but you'd need to factor in the sample rate and amplitude and adjust the script accordingly.

I've previously done a similar thing to this in Node/Javascript in a seperate repo: https://github.com/jabituyaben/Espruino-HRV and a lot of this broadly follows the same structure so the Readme might be helpful there.

But Python has much better purpose built libraries that can be leveraged, particularly hrvanalysis: https://github.com/Aura-healthcare/hrvanalysis

The signal_processing script basically follows these steps: 1. moving average to remove noise/smooth the signal slightly 2. B-Spline interpolation using scipy 3. peak finding with scipy 4. remove outliers and then 5. use hrvanalysis to extract time domain features. The script also saves a log file at each stage and I've kept that in here as it might help with debugging if you get weird results and need to fine tune anything.

If you're interested in looking at frequency domain features using hrvanalysis you'd need to have pretty decent and clean-ish data over a longer duration - the above is a bit quick and dirty because that's the kinda guy I am. When you ommit outliers for that, you're better off using the methods built into the hrvanalysis library than what I've done as the functions in the library backfill omissions with interpolated values where needed. Will look into this at somepoint.
