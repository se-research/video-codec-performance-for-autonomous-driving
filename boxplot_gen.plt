set terminal png size 800, 400

# check output filename parameter
if (!exists("output_file")) output_file='default.pdf'
set output output_file

# Check input file
set style data boxplot 

# Setting the delimiter
set datafile separator ";"

#set title "sequence_1"
set tics font "helvetica,10"

set lmargin screen 0.3

set xrange [0:9]
show xrange

unset key
set border 2
set ytics nomirror

set multiplot

# SSIM boxplot
set style fill solid 0.5 border -1
set style boxplot nooutliers

set xtics ('' 3)
set ylabel 'SSIM value' offset 3, 0 textcolor rgb "red"
set yrange [0.5:1]

plot input1 using (3):11 lc rgb "red"

# Frame size boxplot
set xtics (input1 2) scale 0.0
set ylabel 'Frame size [bytes]' offset -3, 0 textcolor rgb "green"
set ytics offset -6, 0

set yrange [0:65500]
plot input1 using (2):7 lc rgb "green"

# Duration box plot
set xtics ('' 1) scale 0.0
set xtics scale 0.0
set ylabel 'Duration [ms]' offset -9, 0 textcolor rgb "blue"
set ytics offset -12, 0

set yrange [0:40000]
plot input1  using (1):13 linecolor rgb "blue"

# SSIM boxplot 2

set format y ""
set xtics ('' 6) scale 0.0
set yrange [0.5:1]
unset ylabel
plot input2 using (6):11 lc rgb "red"

# Frame size boxplot 2
set xtics (input2 5) scale 0.0
set yrange [0:65500]
set ytics 
plot input2 using (5):7 lc rgb "green"

# Duration box plot 2
set xtics ('' 4) scale 0.0
set yrange [0:40000]

plot input2  using (4):13 linecolor rgb "blue"

# SSIM boxplot 3

set format y ""
set xtics ('' 9) scale 0.0
set yrange [0.5:1]
unset ylabel
plot input3 using (9):11 lc rgb "red"

# Frame size boxplot 3
set xtics (input3 8) scale 0.0
set yrange [0:65000]
set ytics
plot input3 using (8):7 lc rgb "green"

# Duration box plot 3
set xtics ('' 7) scale 0.0
set yrange [0:40000]

plot input3  using (7):13 linecolor rgb "blue"


unset multiplot
